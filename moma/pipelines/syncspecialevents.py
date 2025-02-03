import datetime
import logging
import typing

import moma.pipelines as pl

class SpecialEvent(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        slug: str
        salesforce_campaign: str
        release_date: datetime.date
        turn_off_date: datetime.datetime
        created_at: datetime.datetime
        updated_at: datetime.datetime
        emarsys_event_id: str
        name: str
        start_date: datetime.date
        start_time: datetime.datetime

    name='SpecialEvents'
    job_name='import-special-events'
    bq_table_name='special_events'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
            { 'name': 'slug', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'salesforce_campaign', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'release_date', 'type': 'DATE', 'mode': 'NULLABLE' },
            { 'name': 'turn_off_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'emarsys_event_id', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'start_date', 'type': 'DATE', 'mode': 'NULLABLE' },
            { 'name': 'start_time', 'type': 'DATETIME', 'mode': 'NULLABLE' },
        ]
    }

    pg_table_name = 'special_events'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                slug,
                salesforce_campaign,
                to_char(coalesce(release_date, '3000-01-01'::date), 'YYYY-MM-DD') as release_date,
                to_char(coalesce(turn_off_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as turn_off_date,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                emarsys_event_id,
                name,
                to_char(coalesce(start_date, '3000-01-01'::date), 'YYYY-MM-DD') as start_date,
                to_char(coalesce(start_date + start_time, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as start_time
            FROM special_events
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        if d['release_date'] == '3000-01-01':
            d['release_date'] = None
        if d['turn_off_date'] == '3000-01-01 00:00:00.000000':
            d['turn_off_date'] = None
        if d['start_date'] == '3000-01-01':
            d['start_date'] = None
        if d['start_time'] == '3000-01-01 00:00:00.000000':
            d['start_time'] = None
        return d

run = pl.make_runner(SpecialEvent)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

