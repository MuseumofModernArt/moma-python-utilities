import datetime
import json
import logging
import typing

import moma.pipelines as pl

class PaymentDetail(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        uuid: str
        type: str
        status: str
        amount_in_cents: int
        cart_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        properties: dict

    name='PaymentDetails'
    job_name='import-payment-details'
    bq_table_name='payment_details'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'uuid', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'type', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'status', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'amount_in_cents', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'cart_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'properties', 'type': 'JSON', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'payment_details'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                uuid::text,
                type,
                status,
                amount_in_cents,
                cart_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                coalesce(properties, '{{}}'::jsonb)::text as properties
            FROM payment_details
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['properties'] = json.loads(d['properties'])
        return d

run = pl.make_runner(PaymentDetail)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()