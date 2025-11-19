CREATE OR REPLACE TABLE `moma-dw.moma_apps.purchased_tickets`
(
    id STRING NOT NULL,
    event_id STRING,
    ticket_number STRING,
    barcode STRING NOT NULL,
    ticket_type_id STRING,
    external_id STRING,
    name STRING,
    price INT64,
    date STRING,
    status STRING,
    order_id STRING,
    template_id STRING,
    template_name STRING,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    properties JSON,
    rebook_to_date STRING,
    rebook_completed_at TIMESTAMP,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE OR REPLACE TABLE `moma-membership.moma_import.purchased_tickets`
(
    id STRING NOT NULL,
    event_id STRING,
    ticket_number STRING,
    barcode STRING NOT NULL,
    ticket_type_id STRING,
    external_id STRING,
    name STRING,
    price INT64,
    date STRING,
    status STRING,
    order_id STRING,
    template_id STRING,
    template_name STRING,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    properties JSON,
    rebook_to_date STRING,
    rebook_completed_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.purchased_tickets`
(
    id STRING NOT NULL,
    event_id STRING,
    ticket_number STRING,
    barcode STRING NOT NULL,
    ticket_type_id STRING,
    external_id STRING,
    name STRING,
    price INT64,
    date STRING,
    status STRING,
    order_id STRING,
    template_id STRING,
    template_name STRING,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    properties JSON,
    rebook_to_date STRING,
    rebook_completed_at TIMESTAMP,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.purchased_tickets`
(
    id STRING NOT NULL,
    event_id STRING,
    ticket_number STRING,
    barcode STRING NOT NULL,
    ticket_type_id STRING,
    external_id STRING,
    name STRING,
    price INT64,
    date STRING,
    status STRING,
    order_id STRING,
    template_id STRING,
    template_name STRING,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    properties JSON,
    rebook_to_date STRING,
    rebook_completed_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);