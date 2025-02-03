import typing
import logging

import moma.pipelines as pl

class AdminUser:
    class Record(typing.NamedTuple):
        id: int
        email: str
        google_id: str

    name='AdminUsers'
    job_name='import-admin-users'
    bq_table_name='admin_users'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
                { 'name': 'email', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'google_id', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name='admin_users'

    def pg_source_query(_begin, _end):
        return f"""
            SELECT
                id,
                email,
                google_id,
                to_char(NOW(), 'YYYY-MM-DD HH24:MI:SS"."US') AS created_at
            FROM admin_users
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(AdminUser)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()