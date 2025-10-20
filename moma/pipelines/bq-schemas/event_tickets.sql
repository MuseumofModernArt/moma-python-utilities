CREATE TABLE `moma-dw.moma_apps.event_tickets` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING varying NOT NULL,
    status STRING varying NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.event_tickets` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING varying NOT NULL,
    status STRING varying NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-apps-staging.moma_import.event_tickets` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING varying NOT NULL,
    status STRING varying NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
