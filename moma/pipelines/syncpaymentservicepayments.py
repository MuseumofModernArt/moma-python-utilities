import datetime
import json
import logging
import typing

import moma.pipelines as pl

class PaymentServicePayments(typing.PaymentServicePayment):
    id: str
    amount: int
    external_reference: str
    currency: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: str
    terminal_id: str
    last_digits: str
    card_token: str
    shopper_reference: str
    card_brand: str
    amount_in_cents: int
    first_name: str
    last_name: str
    email: str
    ip_address: str
    additional_risk_data: dict
    raw_payment_data: dict

    name='PaymentServicePayments'
    job_name='import-payment-service-payments'
    bq_table_name='payment_service_payments'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'amount', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'currency', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'terminal_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'last_digits', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'card_token', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'shopper_reference', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'card_brand', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'amount_in_cents', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'first_name', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'last_name', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'email', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'ip_address', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'additional_risk_data', 'type': 'JSON', 'mode': 'NULLABLE' },
                { 'name': 'raw_payment_data', 'type': 'JSON', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'payment_service.payments'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                amount,
                currency,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                status,
                terminal_id,
                last_digits,
                card_token,
                shopper_reference,
                card_brand,
                amount_in_cents,
                first_name,
                last_name,
                email,
                ip_address,
                coalesce(additional_risk_data, '{{}}'::jsonb)::text as additional_risk_data,
                coalesce(raw_payment_data, '{{}}'::jsonb)::text as raw_payment_data
            FROM payment_service.payments
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['additional_risk_data'] = json.loads(d['additional_risk_data'])
        d['raw_payment_data'] = json.loads(d['raw_payment_data'])
        return d

run = pl.make_runner(PaymentServicePayments)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()