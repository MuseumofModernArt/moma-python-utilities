import datetime
import logging
import typing

import moma.pipelines as pl

class SpecialEventTicket(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        name: str
        dollar_amount: int
        identifier: str
        status: str
        contribution_level_id: int
        line_item_id: int
        special_event_id: int
        created_at: datetime.datetime
        updated_at: datetime.datetime

    name='SpecialEventTickets'
    job_name='import-special-event-tickets'
    bq_table_name='special_event_tickets'
    bq_table_schema={
        'fields': [
            { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED' },
            { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'dollar_amount', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'identifier', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE' },
            { 'name': 'contribution_level_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'line_item_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'special_event_id', 'type': 'INTEGER', 'mode': 'NULLABLE' },
            { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
            { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
        ]
    }

    pg_table_name = 'special_event_tickets'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                special_event_tickets.id AS id,
                special_event_tickets.name AS name,
                special_event_tickets.dollar_amount AS dollar_amount,
                special_event_tickets.identifier AS identifier,
                CASE WHEN special_event_tickets.status=0 THEN 'reserved'
                     WHEN special_event_tickets.status=1 THEN 'purchased'
                     WHEN special_event_tickets.status=2 THEN 'refunded'
                     WHEN special_event_tickets.status=3 THEN 'refunding'
                END as status,
                special_event_tickets.contribution_level_id AS contribution_level_id,
                special_event_tickets.line_item_id AS line_item_id,
                contribution_levels.special_event_id AS special_event_id,
                to_char(special_event_tickets.created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(special_event_tickets.updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at
            FROM special_event_tickets
                INNER JOIN contribution_levels ON special_event_tickets.contribution_level_id = contribution_levels.id
            WHERE special_event_tickets.updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(SpecialEventTicket)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

