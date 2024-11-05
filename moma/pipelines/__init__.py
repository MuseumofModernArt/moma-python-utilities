import argparse
import datetime
import importlib
import logging
import os
import pprint
import sys

from dataclasses import dataclass

from google.cloud import bigquery
from google.cloud import secretmanager

from apache_beam.options.pipeline_options import _BeamArgumentParser, GoogleCloudOptions
from apache_beam.io.jdbc import ReadFromJdbc

import apache_beam as beam

from apache_beam.typehints.schemas import LogicalType
from apache_beam.typehints.schemas import MillisInstant

LogicalType.register_logical_type(MillisInstant)

secret_client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_name):
    secret_response = secret_client.access_secret_version(request={'name': secret_name})
    return secret_response.payload.data.decode('UTF-8')

_pp = pprint.PrettyPrinter(indent=2, stream=sys.stdout)

_default_ts = datetime.datetime.fromisoformat('2000-01-01 00:00:00.000+00:00')
@dataclass
class PipelineStatus:
    name: str
    uuid: str
    status: str
    began_at: datetime.datetime

    def __init__(self, name=None, uuid=None, status=None, began_at=_default_ts):
        self.name=name,
        self.uuid=uuid,
        self.status=status,
        self.began_at=began_at

_overlap = datetime.timedelta(minutes=5)

class SyncPipelineOptions(GoogleCloudOptions):
    @classmethod
    def _add_argparse_args(cls, parser: _BeamArgumentParser) -> None:
        parser.add_argument('--jdbc-password-secret', dest='jdbc_password_secret')
        parser.add_argument('--jdbc-username', dest='jdbc_username')
        parser.add_argument('--jdbc-url', dest='jdbc_url')
        parser.add_argument('--pipeline', dest='pipeline')
        parser.add_argument('--temp-project', dest='temp_project')
        parser.add_argument('--destination-project', dest='dest_project')
        parser.add_argument('--destination-dataset', dest='dest_dataset', default='moma')

def make_runner(model, runner_options=None):
    def run(argv=None):
        global pipeline_options

        if runner_options is None:
            options = SyncPipelineOptions()
        else:
            options = runner_options
        pipeline_options = options.view_as(SyncPipelineOptions)

        project = pipeline_options.project
        temp_project = pipeline_options.temp_project
        if temp_project is None:
            temp_project = project

        dest_project = pipeline_options.dest_project
        if dest_project is None:
            dest_project = project

        dest_dataset = pipeline_options.dest_dataset

        job_name = model.job_name

        last_pipeline_status = get_last_successful_pipeline_status(job_name, temp_project)
        status = PipelineStatus(name=job_name, status='started')
        new_pipeline_status = upsert_pipeline_status(status, temp_project)

        print('last pipeline status')
        _pp.pprint(last_pipeline_status)
        print('new pipeline status (starting)')
        _pp.pprint(new_pipeline_status)

        begin = last_pipeline_status.began_at - _overlap
        end = new_pipeline_status.began_at

        pipeline = beam.Pipeline(options=options)

        (
            pipeline |
                f'Get{model.name}Data' >> data_source(model, begin, end) |
                beam.Map(model.to_dict) |
                f'Write{model.name}ToBQ' >> data_sink(model)
        )
        result = pipeline.run()
        result.wait_until_finish()

        source = f'{temp_project}.moma_import.{model.bq_table_name}'
        destination = f'{dest_project}.{dest_dataset}.{model.bq_table_name}'
        bigquery_merge(source, destination, model._fields)

        new_pipeline_status.status = 'success'
        new_pipeline_status = upsert_pipeline_status(new_pipeline_status, temp_project)

        print('new pipeline status (finished)')
        _pp.pprint(new_pipeline_status)
    return run

def data_source(model, begin, end):
    return postgres_source(
        table_name=model.pg_table_name,
        query=model.pg_source_query(begin, end)
    )

def data_sink(model):
    return bigquery_sink(
        table_name=f'{pipeline_options.temp_project}:moma_import.{model.bq_table_name}',
        table_schema=model.bq_table_schema
    )

def postgres_source(table_name, query):
    password = get_secret(f'projects/{pipeline_options.jdbc_password_secret}/versions/1')

    return ReadFromJdbc(
        table_name=table_name,
        driver_class_name='org.postgresql.Driver',
        jdbc_url=pipeline_options.jdbc_url,
        username=pipeline_options.jdbc_username,
        password=password,
        query=query
    )

def bigquery_sink(table_name, table_schema=None):
    return beam.io.gcp.bigquery.WriteToBigQuery(
        table_name,
        schema=table_schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
        create_disposition=beam.io.BigQueryDisposition.CREATE_NEVER,
        )

def bigquery_merge(source, target, fields):
    client = bigquery.Client()
    fields_s = ', '.join(fields)
    update_clauses = ', '.join([f'{f} = S.{f}' for f in fields])
    query = f"""
        DECLARE partition_window STRUCT<min TIMESTAMP, max TIMESTAMP>;

        SET partition_window = (
            SELECT
                STRUCT(min(created_at) AS min, max(created_at) AS max)
            FROM `{source}`
            WHERE created_at BETWEEN TIMESTAMP('2000-01-01 00:00:00+00') AND CURRENT_TIMESTAMP());

        MERGE INTO `{target}` T
        USING (
            SELECT *
            FROM `{source}`
            WHERE created_at BETWEEN partition_window.min AND partition_window.max
        ) S
        ON T.id = S.id
            AND T.created_at BETWEEN partition_window.min AND partition_window.max
        WHEN MATCHED
        THEN
            UPDATE SET {update_clauses}
        WHEN NOT MATCHED
        THEN
            INSERT ({fields_s})
            VALUES ({fields_s});

        TRUNCATE TABLE `{source}`;
    """
    return client.query_and_wait(query)

def get_last_successful_pipeline_status(job_name, project):
    client = bigquery.Client()
    rows = client.query_and_wait(f"""
        SELECT name, uuid, status, began_at
        FROM {project}.moma_import.pipeline_status
        WHERE status = 'success' AND name = @name
        ORDER BY began_at DESC
        LIMIT 1
    """, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', job_name)
        ]
    ))

    pipeline_status = PipelineStatus(name=job_name)
    for row in rows:
        pipeline_status.uuid = row['uuid']
        pipeline_status.status = row['status']
        pipeline_status.began_at = row['began_at']

    return pipeline_status

def upsert_pipeline_status(pipeline_status, project):
    client = bigquery.Client()
    target = f'{project}.moma_import.pipeline_status'
    rows = client.query_and_wait(f"""
        DECLARE target_uuid STRING;

        SET target_uuid = (SELECT COALESCE(@uuid, GENERATE_UUID()));

        MERGE `{target}` T
        USING (
            SELECT
                @name AS name,
                target_uuid AS uuid,
                @status AS status,
                @began_at AS began_at
        ) S
        ON T.uuid = S.uuid AND T.name = S.name
        WHEN NOT MATCHED THEN -- insert a pipeline_status with a new uuid and timestamp
            INSERT (name, uuid, status, began_at)
            VALUES (name, target_uuid, status, CURRENT_TIMESTAMP())
        WHEN MATCHED THEN
            UPDATE SET status = S.status;

        SELECT * FROM `{target}` WHERE name = @name AND uuid = target_uuid;
    """, job_config=bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('name', 'STRING', pipeline_status.name),
            bigquery.ScalarQueryParameter('uuid', 'STRING', pipeline_status.uuid),
            bigquery.ScalarQueryParameter('status', 'STRING', pipeline_status.status),
            bigquery.ScalarQueryParameter('began_at', 'TIMESTAMP', pipeline_status.began_at),
        ]
    ))

    pipeline_status = None
    for row in rows:
        pipeline_status = PipelineStatus(
            name=row['name'],
            uuid=row['uuid'],
            status=row['status'],
            began_at=row['began_at'],
        )
    return pipeline_status

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    pipeline = os.environ.get("PIPELINE")

    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline', dest='pipeline')
    args, _ = parser.parse_known_args()
    if not args.pipeline is None:
        pipeline = args.pipeline

    match pipeline:
        case "admin_users":
            syncadminusers = importlib.import_module('moma.pipelines.syncadminusers')
            make_runner(syncadminusers.AdminUser)()
        case "carts":
            synccarts = importlib.import_module('moma.pipelines.synccarts')
            make_runner(synccarts.Cart)()
        case "line_items":
            synclineitems = importlib.import_module('moma.pipelines.synclineitems')
            make_runner(synclineitems.LineItem)()
        case "login_methods":
            syncloginmethods = importlib.import_module('moma.pipelines.syncloginmethods')
            make_runner(syncloginmethods.LoginMethod)()
        case "payment_details":
            syncpaymentdetails = importlib.import_module('moma.pipelines.syncpaymentdetails')
            make_runner(syncpaymentdetails.PaymentDetail)()
        case "users":
            syncusers = importlib.import_module('moma.pipelines.syncusers')
            make_runner(syncusers.User)()
        case "virtual_queues":
            syncvirtualqueues = importlib.import_module('moma.pipelines.syncvirtualqueues')
            make_runner(syncvirtualqueues.VirtualQueue)()
        case "virtual_queue_participants":
            syncvirtualqueueparticipants = importlib.import_module('moma.pipelines.syncvirtualqueueparticipants')
            make_runner(syncvirtualqueueparticipants.VirtualQueueParticipant)()