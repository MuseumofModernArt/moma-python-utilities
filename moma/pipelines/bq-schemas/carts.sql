--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.carts`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.carts`
(
  id INT64 NOT NULL,
  uuid STRING(72) NOT NULL,
  status STRING NOT NULL,
  contact_id STRING,
  fallback_contact_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  admin_user_id INT64,
  account_id STRING,
  fallback_account_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (admin_user_id) REFERENCES `moma-dw.moma_apps.admin_users`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.carts`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.carts`
(
  id INT64 NOT NULL,
  uuid STRING(72) NOT NULL,
  status STRING NOT NULL,
  contact_id STRING,
  fallback_contact_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  admin_user_id INT64,
  account_id STRING,
  fallback_account_id STRING,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.carts`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.carts`
(
  id INT64 NOT NULL,
  uuid STRING(72) NOT NULL,
  status STRING NOT NULL,
  contact_id STRING,
  fallback_contact_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  admin_user_id INT64,
  account_id STRING,
  fallback_account_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (admin_user_id) REFERENCES `moma-dw.moma_apps_staging.admin_users`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.carts`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.carts`
(
  id INT64 NOT NULL,
  uuid STRING(72) NOT NULL,
  status STRING NOT NULL,
  contact_id STRING,
  fallback_contact_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  admin_user_id INT64,
  account_id STRING,
  fallback_account_id STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);