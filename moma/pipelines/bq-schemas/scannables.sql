--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.scannables`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.scannables`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  scannable_id STRING,
  scannable_type STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.scannables`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.scannables`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  scannable_id STRING,
  scannable_type STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.scannables`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.scannables`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  scannable_id STRING,
  scannable_type STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.scannables`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.scannables`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  scannable_id STRING,
  scannable_type STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);