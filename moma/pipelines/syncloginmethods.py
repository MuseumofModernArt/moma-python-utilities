import datetime
import logging
import typing

import moma.pipelines as pl

class LoginMethod(typing.NamedTuple):
    id: int
    oauth_token: str
    auth0_reference: str
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    name='LoginMethods'
    job_name='import-login-methods'
    bq_table_name='login_methods'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            { 'name': 'oauth_token', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'auth0_reference', 'type': 'STRING', 'mode': 'NULLABLE'},
            { 'name': 'user_id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
        ]
    }

    pg_table_name = 'login_methods'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                oauth_token,
                auth0_reference,
                user_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM login_methods
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(LoginMethod)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()