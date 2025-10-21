import datetime
import logging
import typing

import moma.pipelines as pl

class Event:
    class Record(typing.NamedTuple):
        id: int
        slug: str
        name: str
        cart_timeout_in_minutes: int
        salesforce_campaign: str
        order_quantity_limit: int
        emarsys_event_id: str
        turn_off_date: datetime.datetime
        contact_us_error_msg: str
        location: str
        exhibition: str
        login_enabled: bool
        login_cta: str
        login_prompt_copy: str
        login_features_copy: str
        title: str
        title_enabled: bool
        start_date: datetime.datetime
        start_time: datetime.datetime
        hero_image_url_enabled: bool
        hero_image_url: str
        non_refundable_copy: str
        require_mailing_address: bool
        require_phone_number: bool
        reminder_email_enabled: bool
        created_at: datetime.datetime
        updated_at: datetime.datetime
        price_list_id: int
        event_type: str
        allow_museum_admission: bool
        reminder_emarsys_event_id: str

    name='Events'
    job_name='import-events'
    bq_table_name='events'
    bq_table_schema={
        [
            {'name': 'id', 'type': 'INT64', 'mode': 'REQUIRED'},
            {'name': 'slug', 'type': 'STRING', 'mode': 'REQUIRED'},
            {'name': 'name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'cart_timeout_in_minutes', 'type': 'INT64', 'mode': 'REQUIRED'},
            {'name': 'salesforce_campaign', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'order_quantity_limit', 'type': 'INT64', 'mode': 'NULLABLE'},
            {'name': 'emarsys_event_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'turn_off_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            {'name': 'contact_us_error_msg', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'location', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'exhibition', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'login_enabled', 'type': 'BOOL', 'mode': 'REQUIRED'},
            {'name': 'login_cta', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'login_prompt_copy', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'login_features_copy', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'title', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'title_enabled', 'type': 'BOOL', 'mode': 'NULLABLE'},
            {'name': 'start_date', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            {'name': 'start_time', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'},
            {'name': 'hero_image_url_enabled', 'type': 'BOOL', 'mode': 'NULLABLE'},
            {'name': 'hero_image_url', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'non_refundable_copy', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'require_mailing_address', 'type': 'BOOL', 'mode': 'REQUIRED'},
            {'name': 'require_phone_number', 'type': 'BOOL', 'mode': 'REQUIRED'},
            {'name': 'reminder_email_enabled', 'type': 'BOOL', 'mode': 'REQUIRED'},
            {'name': 'created_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
            {'name': 'updated_at', 'type': 'TIMESTAMP', 'mode': 'REQUIRED'},
            {'name': 'price_list_id', 'type': 'INT64', 'mode': 'NULLABLE'},
            {'name': 'event_type', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'allow_museum_admission', 'type': 'BOOL', 'mode': 'NULLABLE'},
            {'name': 'reminder_emarsys_event_id', 'type': 'STRING', 'mode': 'NULLABLE'}
        ]
  }

    pg_table_name = 'events'

    def pg_source_query(begin, end):
        return f"""
            SELECT
                id,
                slug,
                name,
                cart_timeout_in_minutes,
                salesforce_campaign,
                order_quantity_limit,
                emarsys_event_id,
                turn_off_date,
                contact_us_error_msg,
                location,
                exhibition,
                login_enabled,
                login_cta,
                login_prompt_copy,
                login_features_copy,
                title,
                title_enabled,
                start_date,
                start_time,
                hero_image_url_enabled,
                hero_image_url,
                non_refundable_copy,
                require_mailing_address,
                require_phone_number,
                reminder_email_enabled,
                to_char(created_at, 'YYYY-MM-DD HH24:MI:SS"."US') as created_at,
                to_char(updated_at, 'YYYY-MM-DD HH24:MI:SS"."US') as updated_at,
                price_list_id,
                event_type,
                allow_museum_admission,
                reminder_emarsys_event_id
            FROM events
            WHERE updated_at >= timestamp '{begin.isoformat()}';
        """

    def to_dict(row):
        return row._asdict()

run = pl.make_runner(Event)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()