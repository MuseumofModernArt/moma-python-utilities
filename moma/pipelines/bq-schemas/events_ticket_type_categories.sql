CREATE TABLE public.events_ticket_type_categories (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    ticket_type_category_id INT64 NOT NULL,
    max_quantity INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


