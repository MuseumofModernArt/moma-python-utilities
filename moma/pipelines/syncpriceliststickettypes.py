import datetime
import logging
import typing

import moma.pipelines as pl

class PriceListsTicketType:
    class Record(typing.NamedTuple):
        id: int
        display_order: int
        price_list_id: int
        ticket_type_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='PriceListsTicketTypes'
    job_name='import-price-lists-ticket-types'
    bq_table_name='price-lists-ticket-types'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'display_order', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'price_list_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'ticket_type_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'price-lists-ticket-types'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                display_order,
                price_list_id,
                ticket_type_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM price_lists_ticket_types
            WHERE updated_at >= timestamp '{begin.isoformat()}';ß
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(PriceListsTicketType)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()