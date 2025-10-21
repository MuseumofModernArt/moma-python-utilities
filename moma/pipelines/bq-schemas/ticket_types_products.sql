CREATE TABLE `moma-dw.moma_apps.ticket_types_products` (
    id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    product_sfid STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_id) REFERENCES `moma-dw.moma_apps.ticket_types`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-membership.moma_imports.ticket_types_products` (
    id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    product_sfid STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.ticket_types_products` (
    id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    product_sfid STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_id) REFERENCES `moma-dw.moma_apps_staging.ticket_types`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.ticket_types_products` (
    id INT64 NOT NULL,
    ticket_type_id INT64 NOT NULL,
    product_sfid STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
