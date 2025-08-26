import datetime
import json
import logging
import typing

import moma.pipelines as pl

class Refund(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: str
        payment_detail_id: int
        idempotency_key: str
        amount_in_cents: int
        status: str
        ticket_numbers: list
        line_items: dict
        created_at: datetime.datetime
        updated_at: datetime.datetime
        additional_notes: str
        reason: int
        issued_by: str
        customer_email: str
        cc_email: str

    name='Refunds'
    job_name='import-refunds'
    bq_table_name='refunds'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'payment_detail_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'idempotency_key', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'amount_in_cents', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'ticket_numbers', 'type': 'JSON', 'mode': 'NULLABLE' },
                { 'name': 'line_items', 'type': 'JSON', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'additional_notes', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'reason', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'issued_by', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'customer_email', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'cc_email', 'type': 'STRING', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'refunds'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id::text,
                payment_detail_id,
                idempotency_key,
                amount_in_cents,
                status,
                coalesce(ticket_numbers, '[]'::jsonb)::text as ticket_numbers,
                coalesce(line_items, '{{}}'::jsonb)::text as line_items,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                additional_notes,
                reason,
                issued_by,
                customer_email,
                cc_email
            FROM refunds
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['ticket_numbers'] = json.loads(d['ticket_numbers'])
        d['line_items'] = json.loads(d['line_items'])
        return d

run = pl.make_runner(Refund)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()