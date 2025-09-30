--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.virtual_queues`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.virtual_queues`
(
  id INT64 NOT NULL,
  display_title_public STRING,
  max_capacity INT64,
  status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  slug STRING,
  opening_date TIMESTAMP,
  closing_date TIMESTAMP,
  timeout_in_minutes INT64,
  PRIMARY KEY (id) NOT ENFORCED,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE `moma-membership.moma_import.virtual_queues`
CREATE OR REPLACE TABLE `moma-membership.moma_import.virtual_queues`
(
    id INT64 NOT NULL,
    display_title_public STRING,
    max_capacity INT64,
    status STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    slug STRING,
    opening_date TIMESTAMP,
    closing_date TIMESTAMP,
    timeout_in_minutes INT64,
    PRIMARY KEY (id) NOT ENFORCED,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.virtual_queues`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.virtual_queues`
(
  id INT64 NOT NULL,
  display_title_public STRING,
  max_capacity INT64,
  status STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  slug STRING,
  opening_date TIMESTAMP,
  closing_date TIMESTAMP,
  timeout_in_minutes INT64,
  PRIMARY KEY (id) NOT ENFORCED,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE `moma-apps-staging.moma_import.virtual_queues`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.virtual_queues`
(
    id INT64 NOT NULL,
    display_title_public STRING,
    max_capacity INT64,
    status STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    slug STRING,
    opening_date TIMESTAMP,
    closing_date TIMESTAMP,
    timeout_in_minutes INT64,
    PRIMARY KEY (id) NOT ENFORCED,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);