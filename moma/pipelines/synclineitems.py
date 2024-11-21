import datetime
import json
import logging
import typing

import moma.pipelines as pl

class LineItem(typing.NamedTuple):
    id: int
    type: str
    quantity: int
    amount_in_cents: int
    discounted_total_in_cents: int
    cart_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    finalized: datetime.datetime
    properties: dict
    delivery_properties: dict

    name='LineItems'
    job_name='import-line-items'
    bq_table_name='line_items'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'type', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'quantity', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'amount_in_cents', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'discounted_total_in_cents', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'cart_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'finalized', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'properties', 'type': 'JSON', 'mode': 'NULLABLE' },
                { 'name': 'delivery_properties', 'type': 'JSON', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'line_items'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                type,
                quantity,
                amount_in_cents,
                discounted_total_in_cents,
                cart_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                to_char(coalesce(finalized, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as finalized,
                coalesce(properties, '{{}}'::jsonb)::text as properties,
                coalesce(delivery_properties, '{{}}'::jsonb)::text as delivery_properties
            FROM line_items
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        if d['finalized'] == '3000-01-01 00:00:00.000000':
            d['finalized'] = None
        d['properties'] = json.loads(d['properties'])
        d['delivery_properties'] = json.loads(d['delivery_properties'])
        return d

run = pl.make_runner(LineItem)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()