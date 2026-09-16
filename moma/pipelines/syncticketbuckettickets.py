import datetime
import logging
import typing

import moma.pipelines as pl

class TicketBucketTicket(typing.NamedTuple):
    class Record(typing.NamedTuple):
        id: int
        bucket_name: str
        product_sfid: str
        name_override: str
        caption: str
        position: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        admission_value: str
        child_ticket: bool
        disables_upsell: bool
        adult: bool
        require_adult: bool
        care_partner: bool
        permit_care_partner: bool
        member: bool
        require_member: bool
        staff: bool
        require_staff: bool
        student_ticket: bool

    name='TicketBucketTickets'
    job_name='import-ticket-bucket-tickets'
    bq_table_name='ticket_bucket_tickets'
    bq_table_schema={
        'fields': [
            {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'}, 
            {'name': 'bucket_name', 'type': 'STRING', 'mode': 'REQUIRED'}, 
            {'name': 'product_sfid', 'type': 'STRING', 'mode': 'REQUIRED'}, 
            {'name': 'name_override', 'type': 'STRING', 'mode': 'NULLABLE'}, 
            {'name': 'caption', 'type': 'STRING', 'mode': 'NULLABLE'}, 
            {'name': 'position', 'type': 'INT64', 'mode': 'REQUIRED'}, 
            {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
            {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'}, 
            {'name': 'admission_value', 'type': 'STRING', 'mode': 'REQUIRED'}, 
            {'name': 'child_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'disables_upsell', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'adult', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'require_adult', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'care_partner', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'permit_care_partner', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'member', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'require_member', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'staff', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'require_staff', 'type': 'BOOL', 'mode': 'REQUIRED'}, 
            {'name': 'student_ticket', 'type': 'BOOL', 'mode': 'REQUIRED'}
       ]
    }

    pg_table_name = 'ticket_bucket_tickets'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                bucket_name,
                product_sfid,
                name_override,
                caption,
                position,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                admission_value,
                child_ticket,
                disables_upsell,
                adult,
                require_adult,
                care_partner,
                permit_care_partner,
                member,
                require_member,
                staff,
                require_staff,
                student_ticket
            FROM ticket_bucket_tickets
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        row['child_ticket'] = row['child_ticket'] == 'true'
        row['disables_upsell'] = row['disables_upsell'] == 'true'
        row['adult'] = row['adult'] == 'true'
        row['require_adult'] = row['require_adult'] == 'true'
        row['care_partner'] = row['care_partner'] == 'true'
        row['permit_care_partner'] = row['permit_care_partner'] == 'true'
        row['member'] = row['member'] == 'true'
        row['require_member'] = row['require_member'] == 'true'
        row['staff'] = row['staff'] == 'true'
        row['require_staff'] = row['require_staff'] == 'true'
        row['student_ticket'] = row['student_ticket'] == 'true'
        return row._asdict()

run = pl.make_runner(TicketBucketTicket)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

