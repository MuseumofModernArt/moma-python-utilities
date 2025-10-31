import datetime
import logging
import typing

import moma.pipelines as pl

class EventTimeSlot:
    class Record(typing.NamedTuple):
        id: int
        event_id: int
        max_quantity: int
        start_time: datetime.datetime
        end_time: datetime.datetime
        created_at: datetime.datetime
        updated_at: datetime.datetime
        member_only: bool

    name='EventTimeSlots'
    job_name='import-event-time-slots'
    bq_table_name='event-time-slots'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'event_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'max_quantity', 'type': 'INT64', 'mode': 'NULLABLE'},
                {'name': 'start_time', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'end_time', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'member_only', 'type': 'BOOL', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'event-time-slots'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                event_id,
                max_quantity,
                to_char(coalesce(start_time, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as start_time,
                to_char(coalesce(end_time, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as end_time,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                member_only::text
            FROM event_time_slots
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['member_only'] = d['member_only'] == 'true'

        if d['start_time'] == '3000-01-01 00:00:00.000000':
            d['start_time'] = None

        if d['end_time'] == '3000-01-01 00:00:00.000000':
            d['end_time'] = None
            
        return d

run = pl.make_runner(EventTimeSlot)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()