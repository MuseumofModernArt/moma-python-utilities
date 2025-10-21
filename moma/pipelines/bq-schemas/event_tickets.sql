CREATE TABLE `moma-dw.moma_apps.event_tickets` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING NOT NULL,
    status STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (line_item_id) REFERENCES `moma-dw.moma_apps.line_items`(id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_id) REFERENCES `moma-dw.moma_apps.ticket_types`(id) NOT ENFORCED,
    FOREIGN KEY (event_time_slot_id) REFERENCES `moma-dw.moma_apps.event_time_slots`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-membership.moma_import.event_tickets` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING NOT NULL,
    status STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.event_tickets` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING NOT NULL,
    status STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (line_item_id) REFERENCES `moma-dw.moma_apps_staging.line_items`(id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_id) REFERENCES `moma-dw.moma_apps_staging.ticket_types`(id) NOT ENFORCED,
    FOREIGN KEY (event_time_slot_id) REFERENCES `moma-dw.moma_apps_staging.event_time_slots`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.event_tickets` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    identifier STRING NOT NULL,
    status STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    user_id INT64,
    rebooked_to_id INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
