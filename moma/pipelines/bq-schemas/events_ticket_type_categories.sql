CREATE TABLE `moma-dw.moma_apps.events_ticket_type_categories` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    ticket_type_category_id INT64 NOT NULL,
    max_quantity INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (event_id) REFERENCES `moma-dw.moma_apps.events`(id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_category_id) REFERENCES `moma-dw.moma_apps.ticket_type_categories`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-membership.moma_import.events_ticket_type_categories` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    ticket_type_category_id INT64 NOT NULL,
    max_quantity INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.events_ticket_type_categories` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    ticket_type_category_id INT64 NOT NULL,
    max_quantity INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (event_id) REFERENCES `moma-dw.moma_apps_staging.events`(id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_category_id) REFERENCES `moma-dw.moma_apps_staging.ticket_type_categories`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.events_ticket_type_categories` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    ticket_type_category_id INT64 NOT NULL,
    max_quantity INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


