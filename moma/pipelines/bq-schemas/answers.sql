CREATE OR REPLACE TABLE `moma-dw.moma_apps.answers` (
    id INT64 NOT NULL,
    question_id INT64,
    line_item_id INT64,
    user_id INT64,
    event_id INT64,
    type STRING NOT NULL,
    question_text STRING NOT NULL,
    `values` ARRAY<STRING>,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = FALSE);

CREATE OR REPLACE TABLE `moma-membership.moma_import.answers` (
    id INT64 NOT NULL,
    question_id INT64,
    line_item_id INT64,
    user_id INT64,
    event_id INT64,
    type STRING NOT NULL,
    question_text STRING NOT NULL,
    `values` ARRAY<STRING>,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = FALSE);

CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.answers` (
    id INT64 NOT NULL,
    question_id INT64,
    line_item_id INT64,
    user_id INT64,
    event_id INT64,
    type STRING NOT NULL,
    question_text STRING NOT NULL,
    `values` ARRAY<STRING>,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = FALSE);

CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.answers` (
    id INT64 NOT NULL,
    question_id INT64,
    line_item_id INT64,
    user_id INT64,
    event_id INT64,
    type STRING NOT NULL,
    question_text STRING NOT NULL,
    `values` ARRAY<STRING>,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = FALSE);
