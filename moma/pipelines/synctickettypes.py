import datetime
import logging
import typing

import moma.pipelines as pl

class TicketType:
    class Record(typing.NamedTuple):
        id: int
        name: str
        caption: str
        price_in_cents: int
        ticket_identifier: str
        visible: bool
        comp: bool
        prior_days_can_sell_tickets: int
        event_user_max_quantity: int
        adult_ticket: bool
        require_adult_ticket: bool
        member_ticket: bool
        require_member_ticket: bool
        care_partner: bool
        permit_care_partner: bool
        created_at: datetime.datetime
        updated_at: datetime.datetime
        internal_name: str
        ticket_type_category_id: int
        tax_deductible_amount_in_cents: int
        general_ledger_account: str
        general_ledger_designation: str
        require_child_ticket: bool

    name='TicketTypes'
    job_name='import-ticket-types'
    bq_table_name='ticket-types'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'name', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'caption', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'price_in_cents', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'ticket_identifier', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'visible', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'comp', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'prior_days_can_sell_tickets', 'type': 'INT64', 'mode': 'NULLABLE'},
                {'name': 'event_user_max_quantity', 'type': 'INT64', 'mode': 'NULLABLE'},
                {'name': 'adult_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'require_adult_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'member_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'require_member_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'care_partner', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'permit_care_partner', 'type': 'BOOL', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'internal_name', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'ticket_type_category_id', 'type': 'INT64', 'mode': 'NULLABLE'},
                {'name': 'tax_deductible_amount_in_cents', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'general_ledger_account', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'general_ledger_designation', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'require_child_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'}
            ]
        }

    pg_table_name = 'ticket-types'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                name,
                caption,
                price_in_cents,
                ticket_identifier,
                visible::text,
                comp::text,
                prior_days_can_sell_tickets,
                event_user_max_quantity,
                adult_ticket::text,
                require_adult_ticket::text,
                member_ticket::text,
                require_member_ticket::text,
                care_partner::text,
                permit_care_partner::text,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                internal_name,
                ticket_type_category_id,
                tax_deductible_amount_in_cents,
                general_ledger_account,
                general_ledger_designation,
                require_child_ticket::text
            FROM ticket_types
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['visible'] = d['visible'] == 'true'
        d['comp'] = d['comp'] == 'true'
        d['adult_ticket'] = d['adult_ticket'] == 'true'
        d['require_adult_ticket'] = d['require_adult_ticket'] == 'true'
        d['member_ticket'] = d['member_ticket'] == 'true'
        d['require_member_ticket'] = d['require_member_ticket'] == 'true'
        d['care_partner'] = d['care_partner'] == 'true'
        d['permit_care_partner'] = d['permit_care_partner'] == 'true'
        d['require_child_ticket'] = d['require_child_ticket'] == 'true'

        return d

run = pl.make_runner(TicketType)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()