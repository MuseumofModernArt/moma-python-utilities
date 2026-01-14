CREATE TABLE `moma-dw.moma_apps.gift_membership_batches` (
    id INT64 NOT NULL,
    batch_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    amount INT64 NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    admin_user_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    available_in_mla BOOL DEFAULT true NOT NULL,
    bulk_salesforce_id STRING,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-membership.moma_import.gift_membership_batches` (
    id INT64 NOT NULL,
    batch_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    amount INT64 NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    admin_user_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    available_in_mla BOOL DEFAULT true NOT NULL,
    bulk_salesforce_id STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.gift_membership_batches` (
    id INT64 NOT NULL,
    batch_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    amount INT64 NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    admin_user_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    available_in_mla BOOL DEFAULT true NOT NULL,
    bulk_salesforce_id STRING,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-apps-staging.moma_import.gift_membership_batches` (
    id INT64 NOT NULL,
    batch_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    amount INT64 NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    admin_user_id INT64 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    available_in_mla BOOL DEFAULT true NOT NULL,
    bulk_salesforce_id STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);