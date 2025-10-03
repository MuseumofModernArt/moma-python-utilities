import datetime
import logging
import typing

import moma.pipelines as pl

class ContributionLevel(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        special_event_id: int
        name: str
        caption: str
        dollar_amount: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        quantity_limit: int
        tax_deductible_dollar_amount: int
        ticket_identifier: str
        visible: bool
        number_of_guests: int
        display_order: int
        order_quantity_limit: int
        comp: bool
        concierge_ticket: bool

    name='ContributionLevel'
    job_name='import-contribution-levels'
    bq_table_name='contribution_levels'
    bq_table_schema={
           'fields': [
                { 'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED' },
                { 'name': 'special_event_id', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'caption', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'dollar_amount', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE' },
                { 'name': 'quantity_limit', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'tax_deductible_dollar_amount', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'ticket_identifier', 'type': 'STRING', 'mode': 'NULLABLE' },
                { 'name': 'visible', 'type': 'BOOL', 'mode': 'NULLABLE' },
                { 'name': 'number_of_guests', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'display_order', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'order_quantity_limit', 'type': 'INT64', 'mode': 'NULLABLE' },
                { 'name': 'comp', 'type': 'BOOL', 'mode': 'NULLABLE' },
                { 'name': 'concierge_ticket', 'type': 'BOOL', 'mode': 'NULLABLE' },
           ]
        }

    pg_table_name = 'contribution_levels'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                special_event_id,
                name,
                caption,
                dollar_amount,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                quantity_limit,
                tax_deductible_dollar_amount,
                ticket_identifier,
                visible::text,
                number_of_guests,
                display_order,
                order_quantity_limit,
                comp::text,
                concierge_ticket::text
            FROM contribution_levels
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['visible'] = d['visible'] == 'true'
        d['comp'] = d['comp'] == 'true'
        d['concierge_ticket'] = d['concierge_ticket'] == 'true'
        return d

run = pl.make_runner(ContributionLevel)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()