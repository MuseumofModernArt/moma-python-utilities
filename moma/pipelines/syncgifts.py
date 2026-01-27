import datetime
import logging
import typing

import moma.pipelines as pl

class Gift:
    class Record(typing.NamedTuple):
        id: int
        address_1: str
        address_2: str
        city: str
        state: str
        country_code: str
        zip: str
        created_at: datetime.datetime
        updated_at: datetime.datetime
        phone_number: str
        gift_start_date: datetime.datetime
        gift_expiration_date: datetime.datetime
        fallback_account_id: str
        notification_email_sent_on: datetime.datetime
        token: str
        notification_email_second_sent_on: datetime.datetime
        notification_email_third_sent_on: datetime.datetime
        membership_start_date: datetime.datetime
        account_id: str

    name='Gifts'
    job_name='import-gifts'
    bq_table_name='gifts'
    bq_table_schema={
            'fields': [
                {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
                {'name': 'address_1', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'address_2', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'city', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'state', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'country_code', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'zip', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'phone_number', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'gift_start_date', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
                {'name': 'gift_expiration_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'fallback_account_id', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'notification_email_sent_on', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'token', 'type': 'STRING', 'mode': 'REQUIRED'},
                {'name': 'notification_email_second_sent_on', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'notification_email_third_sent_on', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'membership_start_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
                {'name': 'account_id', 'type': 'STRING', 'mode': 'NULLABLE'}
            ]
        }

    pg_table_name = 'gifts'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                address_1,
                address_2,
                city,
                state,
                country_code,
                zip,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                phone_number,
                to_char(coalesce(gift_start_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as gift_start_date,
                to_char(coalesce(gift_expiration_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as gift_expiration_date,
                fallback_account_id,
                to_char(coalesce(notification_email_sent_on, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as notification_email_sent_on,
                token,
                to_char(coalesce(notification_email_second_sent_on, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as notification_email_second_sent_on,
                to_char(coalesce(notification_email_third_sent_on, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as notification_email_third_sent_on,
                to_char(coalesce(membership_start_date, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as membership_start_date,
                account_id
            FROM gifts
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        d = row._asdict()
        
        if d['gift_start_date'] == '3000-01-01 00:00:00.000000':
            d['gift_start_date'] = None
        if d['gift_expiration_date'] == '3000-01-01 00:00:00.000000':
            d['gift_expiration_date'] = None
        if d['notification_email_sent_on'] == '3000-01-01 00:00:00.000000':
            d['notification_email_sent_on'] = None
        if d['notification_email_second_sent_on'] == '3000-01-01 00:00:00.000000':
            d['notification_email_second_sent_on'] = None
        if d['notification_email_third_sent_on'] == '3000-01-01 00:00:00.000000':
            d['notification_email_third_sent_on'] = None
        if d['membership_start_date'] == '3000-01-01 00:00:00.000000':
            d['membership_start_date'] = None

        return d

run = pl.make_runner(Gift)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()