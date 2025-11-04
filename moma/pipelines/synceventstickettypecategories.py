import datetime
import logging
import typing

import moma.pipelines as pl

class EventsTicketTypeCategory:
    class Record(typing.NamedTuple):
        id: int
        event_id: int
        ticket_type_category_id: int
        max_quantity: int
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='EventsTicketTypeCategories'
    job_name='import-events-ticket-type-categories'
    bq_table_name='events_ticket_type_categories'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'event_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'ticket_type_category_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'max_quantity', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'events_ticket_type_categories'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                event_id,
                ticket_type_category_id,
                max_quantity,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM events_ticket_type_categories
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(EventsTicketTypeCategory)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()