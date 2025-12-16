--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.scannable_events`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.scannable_events`
(
  id INT64 NOT NULL,
  name STRING,
  admin_user_id INT64,
  scannable_id STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  scan_mode STRING,
  party_size INT64,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (admin_user_id) REFERENCES `moma-dw.moma_apps.admin_users`(id) NOT ENFORCED,
  FOREIGN KEY (scannable_id) REFERENCES `moma-dw.moma_apps.scannables`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.scannable_events`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.scannable_events`
(
  id INT64 NOT NULL,
  name STRING,
  admin_user_id INT64,
  scannable_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  scan_mode STRING,
  party_size INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.scannable_events`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.scannable_events`
(
  id INT64 NOT NULL,
  name STRING,
  admin_user_id INT64,
  scannable_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  scan_mode STRING,
  party_size INT64,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (admin_user_id) REFERENCES `moma-dw.moma_apps_staging.admin_users`(id) NOT ENFORCED,
  FOREIGN KEY (scannable_id) REFERENCES `moma-dw.moma_apps_staging.scannables`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.scannable_events`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.scannable_events`
(
  id INT64 NOT NULL,
  name STRING,
  admin_user_id INT64,
  scannable_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  scan_mode STRING,
  party_size INT64
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);