import datetime
import json
import typing
import logging

import moma.pipelines as pl

class VirtualQueueParticipant(typing.NamedTuple):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    phone_country_code: str
    virtual_queue_id: int
    slots: int
    status: str
    priority: int
    uuid: str
    marketing_opt_in: bool
    user_id: int
    web_push_device_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    receive_sms: bool
    notified_at: datetime.datetime
    visiting_at: datetime.datetime
    admitted_count: int
    cancelled_at: datetime.datetime
    unserved_at: datetime.datetime
    properties: dict

    name='VirtualQueueParticipants'
    job_name='import-virtual-queue-participants'
    bq_table_name='virtual_queue_participants'
    bq_table_schema={
            'fields': [
                { 'name': 'id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
                { 'name': 'first_name', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'last_name', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'email', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'phone_number', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'phone_country_code', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'virtual_queue_id', 'type': 'INTEGER', 'mode': 'REQUIRED'},
                { 'name': 'slots', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                { 'name': 'status', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'priority', 'type': 'INTEGER', 'mode': 'REQUIRED'},
                { 'name': 'uuid', 'type': 'STRING', 'mode': 'NULLABLE'},
                { 'name': 'marketing_opt_in', 'type': 'BOOL', 'mode': 'NULLABLE'},
                { 'name': 'user_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                { 'name': 'web_push_device_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                { 'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'receive_sms', 'type': 'BOOL', 'mode': 'NULLABLE'},
                { 'name': 'notified_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'visiting_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'admitted_count', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                { 'name': 'cancelled_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'unserved_at', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                { 'name': 'properties', 'type': 'JSON', 'mode': 'NULLABLE'},
            ]
        }

    pg_table_name = 'virtual_queue_participants'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                first_name,
                last_name,
                email,
                phone_number,
                phone_country_code,
                virtual_queue_id,
                slots,
                status,
                priority,
                uuid::text,
                marketing_opt_in::text,
                user_id,
                web_push_device_id,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                receive_sms::text,
                to_char(coalesce(notified_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as notified_at,
                to_char(coalesce(visiting_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as visiting_at,
                admitted_count,
                to_char(coalesce(cancelled_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as cancelled_at,
                to_char(coalesce(unserved_at, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as unserved_at,
                coalesce(properties, '{{}}'::jsonb)::text as properties
            FROM virtual_queue_participants
            WHERE updated_at BETWEEN timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        d['notified_at'] = date_guard(d['notified_at'])
        d['visiting_at'] = date_guard(d['visiting_at'])
        d['cancelled_at'] = date_guard(d['cancelled_at'])
        d['unserved_at'] = date_guard(d['unserved_at'])
        d['properties'] = json.loads(d['properties'])
        return d

def date_guard(date):
    if date == '3000-01-01 00:00:00.000000':
        return None
    return date

run = pl.make_runner(VirtualQueueParticipant)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

