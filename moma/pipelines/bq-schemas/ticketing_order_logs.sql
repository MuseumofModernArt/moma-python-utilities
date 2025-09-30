-- PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.ticketing_order_logs`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.ticketing_order_logs`
(
  id STRING(72) NOT NULL,
  request_path STRING NOT NULL,
  request_body STRING NOT NULL,
  response_body STRING,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-dw.moma_apps.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.ticketing_order_logs`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.ticketing_order_logs`
(
  id STRING(72) NOT NULL,
  request_path STRING NOT NULL,
  request_body STRING NOT NULL,
  response_body STRING,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-membership.moma_import.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.ticketing_order_logs`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.ticketing_order_logs`
(
  id STRING(72) NOT NULL,
  request_path STRING NOT NULL,
  request_body STRING NOT NULL,
  response_body STRING,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-dw.moma_apps_staging.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.ticketing_order_logs`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.ticketing_order_logs`
(
  id STRING(72) NOT NULL,
  request_path STRING NOT NULL,
  request_body STRING NOT NULL,
  response_body STRING,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-apps-staging.moma_import.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);