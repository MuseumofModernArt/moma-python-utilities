import datetime
import logging
import typing

import moma.pipelines as pl

class GiftMembershipBatch:
    class Record(typing.NamedTuple):
        id: int
        batch_name: str
        product_sfid: str
        amount: int
        expires_at: datetime.datetime
        admin_user_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        available_in_mla: bool
        bulk_salesforce_id: str

    name='GiftMembershipBatches'
    job_name='import-gift-membership-batches'
    bq_table_name='gift_membership_batches'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'batch_name', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'product_sfid', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'amount', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'expires_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'admin_user_id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'available_in_mla', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
                {'name': 'bulk_salesforce_id', 'type': 'STRING', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'gift_membership_batches'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                batch_name,
                product_sfid,
                amount,
                to_char(coalesce(expires_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as expires_at,
                admin_user_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                available_in_mla::text,
                bulk_salesforce_id
            FROM gift_membership_batches
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        
        if d['expires_at'] == '3000-01-01 00:00:00.000000':
            d['expires_at'] = None

        d['available_in_mla'] = d['available_in_mla'] == 'true'

        return d

run = pl.make_runner(GiftMembershipBatch)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()