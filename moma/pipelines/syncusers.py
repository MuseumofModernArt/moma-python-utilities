import datetime
import logging
import typing

import moma.pipelines as pl

class User(typing.NamedTuple):
    id: int
    active: bool
    email: str
    uuid: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    first_name: str
    last_name: str
    contact_id: str
    fallback_contact_id: str
    account_id: str
    fallback_account_id: str
    external_reference: str
    last_authenticated_on: datetime.datetime

    name='Users'
    job_name='import-users'
    bq_table_name='users'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            { 'name': 'active', 'type': 'BOOL', 'mode': 'REQUIRED'},
            { 'name': 'email', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'uuid', 'type': 'STRING', 'mode': 'REQUIRED'},
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            { 'name': 'first_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'last_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'contact_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'fallback_contact_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'account_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'fallback_account_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'external_reference', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'last_authenticated_on', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
        ]
    }

    pg_table_name = 'users'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                active::text,
                email,
                uuid,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                first_name,
                last_name,
                contact_id,
                fallback_contact_id
                account_id,
                fallback_account_id,
                external_reference,
                to_char(coalesce(last_authenticated_on, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as last_authenticated_on
            FROM users
            WHERE updated_at BETWEEN timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['active'] = d['active'] == 'true'
        if d['last_authenticated_on'] == '3000-01-01 00:00:00.000000':
            d['last_authenticated_on'] = None
        return d

run = pl.make_runner(User)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()