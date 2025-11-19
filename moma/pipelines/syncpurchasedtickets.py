import datetime
import json
import logging
import typing

import moma.pipelines as pl

class PurchasedTicket(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: str
        event_id: str
        ticket_number: str
        barcode: str
        ticket_type_id: str
        external_id: str
        name: str
        price: int
        date: str
        status: str
        order_id: str
        template_id: str
        template_name: str
        created_at: datetime.datetime
        updated_at: datetime.datetime
        properties: dict
        rebook_to_date: str
        rebook_completed_at: datetime.datetime

    name='PurchasedTickets'
    job_name='import-purchased-tickets'
    bq_table_name='purchased_tickets'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' }, 
                { 'name': 'event_id', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'ticket_number', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'barcode', 'type': 'STRING', 'mode': 'REQUIRED' }, 
                { 'name': 'ticket_type_id', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'external_id', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'price', 'type': 'INT64', 'mode': 'NULLABLE' }, 
                { 'name': 'date', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'order_id', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'template_id', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'template_name', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED' }, 
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED' }, 
                { 'name': 'properties', 'type': 'JSON', 'mode': 'NULLABLE' }, 
                { 'name': 'rebook_to_date', 'type': 'STRING', 'mode': 'NULLABLE' }, 
                { 'name': 'rebook_completed_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' }
            ]
        }

    pg_table_name = 'purchased_tickets'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                event_id,
                ticket_number,
                barcode,
                ticket_type_id,
                external_id,
                name,
                price,
                date,
                status,
                order_id,
                template_id,
                template_name,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                coalesce(properties, '{{}}'::jsonb)::text as properties,
                rebook_to_date,
                to_char(coalesce(rebook_completed_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as rebook_completed_at
            FROM purchased_tickets
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['properties'] = json.loads(d['properties'])
        if d['rebook_completed_at'] == '3000-01-01 00:00:00.000000':
            d['rebook_completed_at'] = None
        return d

run = pl.make_runner(PurchasedTicket)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()