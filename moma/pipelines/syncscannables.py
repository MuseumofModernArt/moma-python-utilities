import datetime
import logging
import typing

import moma.pipelines as pl

class Scannable(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        uuid: str
        scannable_id: str
        scannable_type: str
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='Scannables'
    job_name='import-scannables'
    bq_table_name='scannables'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
            { 'name': 'uuid', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'scannable_id', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'scannable_type', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
        ]
    }

    pg_table_name = 'scannables'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                uuid::text,
                scannable_id,
                scannable_type,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM scannables
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(Scannable)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

