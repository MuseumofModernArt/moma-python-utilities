--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.special_events`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.special_events`
(
  id INT64 NOT NULL,
  slug STRING,
  salesforce_campaign STRING,
  release_date DATE,
  turn_off_date TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  emarsys_event_id STRING,
  name STRING,
  start_date DATE,
  start_time DATETIME,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.special_events`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.special_events`
(
  id INT64 NOT NULL,
  slug STRING,
  salesforce_campaign STRING,
  release_date DATE,
  turn_off_date TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  emarsys_event_id STRING,
  name STRING,
  start_date DATE,
  start_time DATETIME
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.special_events`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.special_events`
(
  id INT64 NOT NULL,
  slug STRING,
  salesforce_campaign STRING,
  release_date DATE,
  turn_off_date TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  emarsys_event_id STRING,
  name STRING,
  start_date DATE,
  start_time DATETIME,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.special_events`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.special_events`
(
  id INT64 NOT NULL,
  slug STRING,
  salesforce_campaign STRING,
  release_date DATE,
  turn_off_date TIMESTAMP,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  emarsys_event_id STRING,
  name STRING,
  start_date DATE,
  start_time DATETIME
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);