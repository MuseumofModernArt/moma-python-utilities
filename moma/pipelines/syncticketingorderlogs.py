import datetime
import logging
import typing

import moma.pipelines as pl

class TicketingOrderLog(typing.NamedTuple):
    id: str
    request_path: str
    request_body: str
    response_body: str
    order_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    name='TicketingOrderLogs'
    job_name='import-ticketing-order-logs'
    bq_table_name='ticketing_order_logs'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'request_path', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'request_body', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'response_body', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'order_id', 'type': 'STRING', 'mode': 'REQUIRED' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            ]
        }

    pg_table_name = 'ticketing.order_logs'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id::text,
                request_path,
                request_body,
                response_body,
                order_id::text,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM ticketing.order_logs
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(TicketingOrderLog)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()