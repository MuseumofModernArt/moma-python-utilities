import datetime
import typing
import logging

import moma.pipelines as pl

class TicketingOrder(typing.NamedTuple):
    id: str
    status: int
    customer_id: str
    email: str
    reservation_id: str
    requested_items: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    payment_id: str
    external_id: str
    total_amount: int
    purchase_date: datetime.datetime
    reservation_expires_at: datetime.datetime
    total_refund_amount: int
    sales_channel: str

    name='TicketingOrders'
    job_name='import-ticketing-orders'
    bq_table_name='ticketing_orders'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'status', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'customer_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'email', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'reservation_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'requested_items', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'payment_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'external_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'total_amount', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'purchase_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'reservation_expires_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'total_refund_amount', 'type': 'INTEGER', 'mode': 'NULLABLE' },
                { 'name': 'sales_channel', 'type': 'STRING', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'ticketing.orders'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                status,
                customer_id,
                reservation_id,
                requested_items,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                payment_id,
                external_id,
                total_amount,
                to_char(coalesce(purchase_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as purchase_date,
                to_char(coalesce(reservation_expires_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as reservation_expires_at,
                total_refund_amount,
                sales_channel
            FROM ticketing.orders
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        if d['purchase_date'] == '3000-01-01 00:00:00.000000':
            d['purchase_date'] == None
        if d['reservation_expires_at'] == '3000-01-01 00:00:00.000000':
            d['reservation_expires_at'] == None
        return d

run = pl.make_runner(TicketingOrder)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
