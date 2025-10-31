import datetime
import logging
import typing

import moma.pipelines as pl

class TicketTypesProduct:
    class Record(typing.NamedTuple):
        id: int
        ticket_type_id: int
        product_sfid: str
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='TicketTypesProducts'
    job_name='import-ticket-types-products'
    bq_table_name='ticket_types_products'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'ticket_type_id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'product_sfid', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'ticket_types_products'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                ticket_type_id,
                product_sfid,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM ticket_types_products
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(TicketTypesProduct)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()