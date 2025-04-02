import datetime
import logging
import typing

import moma.pipelines as pl

class TicketingTicket(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: str
        ticket_type_id: str
        name: str
        description: str
        type_of_ticket: str
        price: int
        ticket_number: str
        barcode: str
        date: str
        status: int
        order_id: str
        created_at: datetime.datetime
        updated_at: datetime.datetime
        external_order_item_id: str
        external_id: str
        event_id: str
        template_id: str

    name='TicketingTickets'
    job_name='import-ticketing-tickets'
    bq_table_name='ticketing_tickets'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'ticket_type_id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'description', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'type_of_ticket', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'price', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'ticket_number', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'barcode', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'date', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'status', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'order_id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'external_order_item_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'external_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'event_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'template_id', 'type': 'STRING', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'ticketing.tickets'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id::text,
                ticket_type_id,
                name,
                description,
                type_of_ticket,
                price,
                ticket_number,
                barcode,
                date,
                status,
                order_id::text,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                external_order_item_id,
                external_id,
                event_id,
                template_id
            FROM ticketing.tickets
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(TicketingTicket)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()