import datetime
import logging
import typing

import moma.pipelines as pl

class ScannableEvent(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        name: str
        admin_user_id: int
        scannable_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        scan_mode: str

    name='ScannableEvents'
    job_name='import-scannable-events'
    bq_table_name='scannable_events'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
            { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'admin_user_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'scannable_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'scan_mode', 'type': 'STRING', 'mode': 'NULLABLE' },
        ]
    }

    pg_table_name = 'scannable_events'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                name,
                admin_user_id,
                scannable_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                scan_mode
            FROM scannable_events
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(ScannableEvent)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

