# model tables in bigquery (staging / production)
# python pipeline definition
# run the job locally
# set up the scheduler

import datetime
import typing
import logging

import moma.pipelines as pl

class VirtualQueue(typing.NamedTuple):
    id: int
    display_title_public: str
    max_capacity: int
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    slug: str
    opening_date: datetime.datetime
    closing_date: datetime.datetime
    timeout_in_minutes: int

    name='VirtualQueues'
    job_name='import-virtual-queues'
    bq_table_name='virtual_queues'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'display_title_public', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'max_capacity', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'slug', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'opening_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'closing_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'timeout_in_minutes', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'virtual_queues'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                display_title_public,
                max_capacity,
                status,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                slug,
                to_char(coalesce(opening_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as opening_date,
                to_char(coalesce(closing_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as closing_date,
                timeout_in_minutes
            FROM virtual_queues
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        if d['opening_date'] == '3000-01-01 00:00:00.000000':
            d['opening_date'] = None
        if d['closing_date'] == '3000-01-01 00:00:00.000000':
            d['closing_date'] = None
        return d

run = pl.make_runner(VirtualQueue)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()