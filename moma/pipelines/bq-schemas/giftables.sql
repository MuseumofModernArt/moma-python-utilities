CREATE TABLE `moma-dw.moma_apps.giftable` (
    id INT64 NOT NULL,
    status STRING,
    gift_code STRING NOT NULL,
    expires_at TIMESTAMP,
    purchased_at TIMESTAMP,
    activated_at TIMESTAMP,
    expired_at TIMESTAMP,
    redeemed_at TIMESTAMP,
    refunded_at TIMESTAMP,
    balance_in_cents INT64 DEFAULT 0 NOT NULL,
    purchased_by_id INT64,
    redeemed_by_id INT64,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    gifter_name STRING,
    giftee_name STRING,
    gifter_email STRING,
    giftee_email STRING,
    gift_membership_batch_id INT64,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (redeemed_by_id) REFERENCES `moma-dw.moma_apps.line_items`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-membership.moma_import.giftable` (
    id INT64 NOT NULL,
    status STRING,
    gift_code STRING NOT NULL,
    expires_at TIMESTAMP,
    purchased_at TIMESTAMP,
    activated_at TIMESTAMP,
    expired_at TIMESTAMP,
    redeemed_at TIMESTAMP,
    refunded_at TIMESTAMP,
    balance_in_cents INT64 DEFAULT 0 NOT NULL,
    purchased_by_id INT64,
    redeemed_by_id INT64,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    gifter_name STRING,
    giftee_name STRING,
    gifter_email STRING,
    giftee_email STRING,
    gift_membership_batch_id INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.giftable` (
    id INT64 NOT NULL,
    status STRING,
    gift_code STRING NOT NULL,
    expires_at TIMESTAMP,
    purchased_at TIMESTAMP,
    activated_at TIMESTAMP,
    expired_at TIMESTAMP,
    redeemed_at TIMESTAMP,
    refunded_at TIMESTAMP,
    balance_in_cents INT64 DEFAULT 0 NOT NULL,
    purchased_by_id INT64,
    redeemed_by_id INT64,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    gifter_name STRING,
    giftee_name STRING,
    gifter_email STRING,
    giftee_email STRING,
    gift_membership_batch_id INT64,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (redeemed_by_id) REFERENCES `moma-dw.moma_apps_staging.line_items`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-apps-staging.moma_import.giftable` (
    id INT64 NOT NULL,
    status STRING,
    gift_code STRING NOT NULL,
    expires_at TIMESTAMP,
    purchased_at TIMESTAMP,
    activated_at TIMESTAMP,
    expired_at TIMESTAMP,
    redeemed_at TIMESTAMP,
    refunded_at TIMESTAMP,
    balance_in_cents INT64 DEFAULT 0 NOT NULL,
    purchased_by_id INT64,
    redeemed_by_id INT64,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    delivery_date TIMESTAMP,
    gifter_name STRING,
    giftee_name STRING,
    gifter_email STRING,
    giftee_email STRING,
    gift_membership_batch_id INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);