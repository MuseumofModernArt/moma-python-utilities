--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.users`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.users`
(
  id INT64 NOT NULL,
  active BOOL NOT NULL,
  email STRING,
  uuid STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  first_name STRING,
  last_name STRING,
  contact_id STRING,
  fallback_contact_id STRING,
  account_id STRING,
  fallback_account_id STRING,
  external_reference STRING,
  last_authenticated_on TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.users`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.users`
(
  id INT64 NOT NULL,
  active BOOL NOT NULL,
  email STRING,
  uuid STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  first_name STRING,
  last_name STRING,
  contact_id STRING,
  fallback_contact_id STRING,
  account_id STRING,
  fallback_account_id STRING,
  external_reference STRING,
  last_authenticated_on TIMESTAMP,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.users`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.users`
(
  id INT64 NOT NULL,
  active BOOL NOT NULL,
  email STRING,
  uuid STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  first_name STRING,
  last_name STRING,
  contact_id STRING,
  fallback_contact_id STRING,
  account_id STRING,
  fallback_account_id STRING,
  external_reference STRING,
  last_authenticated_on TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.users`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.users`
(
  id INT64 NOT NULL,
  active BOOL NOT NULL,
  email STRING,
  uuid STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  first_name STRING,
  last_name STRING,
  contact_id STRING,
  fallback_contact_id STRING,
  account_id STRING,
  fallback_account_id STRING,
  external_reference STRING,
  last_authenticated_on TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);