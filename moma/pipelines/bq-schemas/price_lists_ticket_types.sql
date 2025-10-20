CREATE TABLE `moma-dw.moma_apps.price_lists_ticket_types` (
    id INT64 NOT NULL,
    display_order INT64 DEFAULT 0 NOT NULL,
    price_list_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.price_lists_ticket_types` (
    id INT64 NOT NULL,
    display_order INT64 DEFAULT 0 NOT NULL,
    price_list_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.price_lists_ticket_types` (
    id INT64 NOT NULL,
    display_order INT64 DEFAULT 0 NOT NULL,
    price_list_id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
