CREATE TABLE `moma-dw.moma_apps.gifts` (
    id INT64 NOT NULL,
    address_1 STRING NOT NULL,
    address_2 STRING,
    city STRING NOT NULL,
    state STRING,
    country_code STRING DEFAULT 'US' NOT NULL,
    zip STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    phone_number STRING,
    gift_start_date TIMESTAMP NOT NULL,
    gift_expiration_date TIMESTAMP,
    fallback_account_id STRING,
    notification_email_sent_on TIMESTAMP,
    token STRING NOT NULL,
    notification_email_second_sent_on TIMESTAMP,
    notification_email_third_sent_on TIMESTAMP,
    membership_start_date TIMESTAMP,
    account_id STRING,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-membership.moma_import.gifts` (
    id INT64 NOT NULL,
    address_1 STRING NOT NULL,
    address_2 STRING,
    city STRING NOT NULL,
    state STRING,
    country_code STRING DEFAULT 'US' NOT NULL,
    zip STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    phone_number STRING,
    gift_start_date TIMESTAMP NOT NULL,
    gift_expiration_date TIMESTAMP,
    fallback_account_id STRING,
    notification_email_sent_on TIMESTAMP,
    token STRING NOT NULL,
    notification_email_second_sent_on TIMESTAMP,
    notification_email_third_sent_on TIMESTAMP,
    membership_start_date TIMESTAMP,
    account_id STRING,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.gifts` (
    id INT64 NOT NULL,
    address_1 STRING NOT NULL,
    address_2 STRING,
    city STRING NOT NULL,
    state STRING,
    country_code STRING DEFAULT 'US' NOT NULL,
    zip STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    phone_number STRING,
    gift_start_date TIMESTAMP NOT NULL,
    gift_expiration_date TIMESTAMP,
    fallback_account_id STRING,
    notification_email_sent_on TIMESTAMP,
    token STRING NOT NULL,
    notification_email_second_sent_on TIMESTAMP,
    notification_email_third_sent_on TIMESTAMP,
    membership_start_date TIMESTAMP,
    account_id STRING,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-apps-staging.moma_import.gifts` (
    id INT64 NOT NULL,
    address_1 STRING NOT NULL,
    address_2 STRING,
    city STRING NOT NULL,
    state STRING,
    country_code STRING DEFAULT 'US' NOT NULL,
    zip STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    phone_number STRING,
    gift_start_date TIMESTAMP NOT NULL,
    gift_expiration_date TIMESTAMP,
    fallback_account_id STRING,
    notification_email_sent_on TIMESTAMP,
    token STRING NOT NULL,
    notification_email_second_sent_on TIMESTAMP,
    notification_email_third_sent_on TIMESTAMP,
    membership_start_date TIMESTAMP,
    account_id STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);