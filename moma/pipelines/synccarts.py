import datetime
import logging
import typing

import moma.pipelines as pl

class Cart(typing.NamedTuple):
    id: int
    uuid: str
    status: str
    contact_id: str
    fallback_contact_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    admin_user_id: int
    account_id: str
    fallback_account_id: str

    name='Carts'
    job_name='import-carts'
    bq_table_name='carts'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            { 'name': 'uuid', 'type': 'STRING', 'mode': 'REQUIRED'},
            { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'contact_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'fallback_contact_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            { 'name': 'admin_user_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            { 'name': 'account_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'fallback_account_id', 'type': 'STRING', 'mode': 'NULLABLE'},
        ]
    }

    pg_table_name = 'carts'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                uuid,
                status,
                contact_id,
                fallback_contact_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                admin_user_id,
                account_id,
                fallback_account_id
            FROM carts
            WHERE updated_at BETWEEN timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(Cart)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()