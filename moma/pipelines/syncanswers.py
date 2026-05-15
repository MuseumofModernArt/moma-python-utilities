import datetime
import logging
import typing

import moma.pipelines as pl

class Answer:
    class Record(typing.NamedTuple):
        id: int
        question_id: int
        line_item_id: int
        user_id: int
        event_id: int
        type: str
        question_text: str
        values: str
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='Answers'
    job_name='import-answers'
    bq_table_name='answers'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
                {'name': 'question_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'line_item_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'user_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'event_id', 'type': 'INT64', 'mode': 'NULLABLE'}, 
                {'name': 'type', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'question_text', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'values', 'type': 'STRING', 'mode': 'REQUIRED'}, 
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'answers'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                question_id,
                line_item_id,
                user_id,
                event_id,
                type,
                question_text,
                values,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM answers
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(Answer)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()