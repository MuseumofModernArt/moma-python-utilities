-- PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.ticketing_orders`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.ticketing_orders`
(
  id STRING(72) NOT NULL,
  status INT64 NOT NULL,
  customer_id STRING,
  email STRING,
  reservation_id STRING,
  requested_items STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  payment_id STRING,
  external_id STRING,
  total_amount INT64,
  purchase_date TIMESTAMP,
  reservation_expires_at TIMESTAMP,
  total_refund_amount INT64,
  order_number STRING,
  sales_channel STRING,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.ticketing_orders`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.ticketing_orders`
(
  id STRING(72) NOT NULL,
  status INT64 NOT NULL,
  customer_id STRING,
  email STRING,
  reservation_id STRING,
  requested_items STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  payment_id STRING,
  external_id STRING,
  total_amount INT64,
  purchase_date TIMESTAMP,
  reservation_expires_at TIMESTAMP,
  total_refund_amount INT64,
  order_number STRING,
  sales_channel STRING,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.ticketing_orders`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.ticketing_orders`
(
  id STRING(72) NOT NULL,
  status INT64 NOT NULL,
  customer_id STRING,
  email STRING,
  reservation_id STRING,
  requested_items STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  payment_id STRING,
  external_id STRING,
  total_amount INT64,
  purchase_date TIMESTAMP,
  reservation_expires_at TIMESTAMP,
  total_refund_amount INT64,
  order_number STRING,
  sales_channel STRING,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.ticketing_orders`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.ticketing_orders`
(
  id STRING(72) NOT NULL,
  status INT64 NOT NULL,
  customer_id STRING,
  email STRING,
  reservation_id STRING,
  requested_items STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  payment_id STRING,
  external_id STRING,
  total_amount INT64,
  purchase_date TIMESTAMP,
  reservation_expires_at TIMESTAMP,
  total_refund_amount INT64,
  order_number STRING,
  sales_channel STRING,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);