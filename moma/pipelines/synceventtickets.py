import datetime
import logging
import typing

import moma.pipelines as pl

class EventTicket:
    class Record(typing.NamedTuple):
        id: int
        name: str
        price_in_cents: int
        identifier: str
        status: str
        line_item_id: int
        ticket_type_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        event_time_slot_id: int
        user_id: int
        rebooked_to_id: int

    name='EventTickets'
    job_name='import-event-tickets'
    bq_table_name='event_tickets'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'price_in_cents', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'identifier', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'status', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'line_item_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'ticket_type_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'event_time_slot_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'user_id', 'type': 'INT64', 'mode': 'NULLABLE'},
                {'name': 'rebooked_to_id', 'type': 'INT64', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'event_tickets'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                name,
                price_in_cents,
                identifier,
                status,
                line_item_id,
                ticket_type_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                event_time_slot_id,
                user_id,
                rebooked_to_id
            FROM event_tickets
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(EventTicket)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()