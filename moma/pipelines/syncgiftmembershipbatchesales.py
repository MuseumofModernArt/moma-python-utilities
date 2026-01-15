import datetime
import logging
import typing

import moma.pipelines as pl

class GiftMembershipBatchSale:
    class Record(typing.NamedTuple):
        id: int
        gift_membership_batch_id: int
        line_item_type: str
        line_item_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        gift_giver_first_name: str
        gift_giver_last_name: str
        gift_giver_email: str

    name='GiftMembershipBatchSales'
    job_name='import-gift-membership-batch-sales'
    bq_table_name='gift_membership_batch_sales'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'gift_membership_batch_id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'line_item_type', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'line_item_id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
                {'name': 'gift_giver_first_name', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'gift_giver_last_name', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'gift_giver_email', 'type': 'STRING', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'gift_membership_batch_sales'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                gift_membership_batch_id,
                line_item_type,
                line_item_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                gift_giver_first_name,
                gift_giver_last_name,
                gift_giver_email
            FROM gift_membership_batch_sales
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()

        return d

run = pl.make_runner(GiftMembershipBatchSale)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()