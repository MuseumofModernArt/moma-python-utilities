import datetime
import logging
import typing

import moma.pipelines as pl

class PriceList:
    class Record(typing.NamedTuple):
        id: int
        name: str
        description: str
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='PriceLists'
    job_name='import-price-lists'
    bq_table_name='price_lists'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'description', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'price_lists'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                name,
                description,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM price_lists
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(PriceList)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()