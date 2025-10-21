import datetime
import logging
import typing

import moma.pipelines as pl

class EventTimeSlotsProduct:
    class Record(typing.NamedTuple):
        id: int
        event_time_slot_id: int
        product_sfid: str
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='EventTimeSlotsProducts'
    job_name='import-event-time-slots-productss'
    bq_table_name='event-time-slots-productss'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'event_time_slot_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'product_sfid', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'event-time-slots-productss'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                event_time_slot_id,
                product_sfid,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM event_time_slots_productss
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(EventTimeSlotsProduct)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()