CREATE TABLE `moma-dw.moma_apps.gift_membership_batch_sales` (
    id INT64 NOT NULL,
    gift_membership_batch_id INT64 NOT NULL,
    line_item_type STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    gift_giver_first_name STRING,
    gift_giver_last_name STRING,
    gift_giver_email STRING,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (gift_membership_batch_id) REFERENCES `moma-dw.moma_apps.gift_membership_batches`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-membership.moma_import.gift_membership_batch_sales` (
    id INT64 NOT NULL,
    gift_membership_batch_id INT64 NOT NULL,
    line_item_type STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    gift_giver_first_name STRING,
    gift_giver_last_name STRING,
    gift_giver_email STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.gift_membership_batch_sales` (
    id INT64 NOT NULL,
    gift_membership_batch_id INT64 NOT NULL,
    line_item_type STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    gift_giver_first_name STRING,
    gift_giver_last_name STRING,
    gift_giver_email STRING,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (gift_membership_batch_id) REFERENCES `moma-dw.moma_apps_staging.gift_membership_batches`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-apps-staging.moma_import.gift_membership_batch_sales` (
    id INT64 NOT NULL,
    gift_membership_batch_id INT64 NOT NULL,
    line_item_type STRING NOT NULL,
    line_item_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    gift_giver_first_name STRING,
    gift_giver_last_name STRING,
    gift_giver_email STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);