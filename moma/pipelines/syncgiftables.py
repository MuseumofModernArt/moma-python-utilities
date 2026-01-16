import datetime
import logging
import typing

import moma.pipelines as pl

class Giftable:
    class Record(typing.NamedTuple):
        id: int
        status: str
        gift_code: str
        expires_at: datetime.datetime
        purchased_at: datetime.datetime
        activated_at: datetime.datetime
        expired_at: datetime.datetime
        redeemed_at: datetime.datetime
        refunded_at: datetime.datetime
        balance_in_cents: int
        purchased_by_id: int
        redeemed_by_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        delivery_date: datetime.datetime
        gifter_name: str
        giftee_name: str
        gifter_email: str
        giftee_email: str
        gift_membership_batch_id: int

    name='Giftables'
    job_name='import-giftables'
    bq_table_name='giftables'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'gift_code', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'expires_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'purchased_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'activated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'expired_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'redeemed_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'refunded_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'balance_in_cents', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'purchased_by_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'redeemed_by_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'delivery_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'gifter_name', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'giftee_name', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'gifter_email', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'giftee_email', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'gift_membership_batch_id', 'type': 'INT64', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'giftables'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                status,
                gift_code,
                tochar(coalesce(expires_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS expires_at,
                tochar(coalesce(purchased_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS purchased_at,
                tochar(coalesce(activated_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS activated_at,
                tochar(coalesce(expired_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS expired_at,
                tochar(coalesce(redeemed_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS redeemed_at,
                tochar(coalesce(refunded_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS refunded_at
                balance_in_cents,
                purchased_by_id,
                redeemed_by_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,,
                tochar(coalesce(delivery_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') AS delivery_date,
                gifter_name,
                giftee_name,
                gifter_email,
                giftee_email,
                gift_membership_batch_id
            FROM giftables
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        
        if d['expires_at'] == '3000-01-01 00:00:00.000000':           
            d['expires_at'] = None

        if d['purchased_at'] == '3000-01-01 00:00:00.000000':
            d['purchased_at'] = None

        if d['activated_at'] == '3000-01-01 00:00:00.000000':
            d['activated_at'] = None

        if d['expired_at'] == '3000-01-01 00:00:00.000000':
            d['expired_at'] = None

        if d['redeemed_at'] == '3000-01-01 00:00:00.000000':
            d['redeemed_at'] = None
            
        if d['delivery_date'] == '3000-01-01 00:00:00.000000':
            d['delivery_date'] = None

        if d['refunded_at'] == '3000-01-01 00:00:00.000000':
            d['refunded_at'] = None

        return d

run = pl.make_runner(Giftable)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()