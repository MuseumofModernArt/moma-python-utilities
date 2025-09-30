--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.payment_details`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.payment_details`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  type STRING NOT NULL,
  status STRING NOT NULL,
  amount_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (cart_id) REFERENCES `moma-dw.moma_apps.carts`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.payment_details`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.payment_details`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  type STRING NOT NULL,
  status STRING NOT NULL,
  amount_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  properties JSON
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.payment_details`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.payment_details`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  type STRING NOT NULL,
  status STRING NOT NULL,
  amount_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (cart_id) REFERENCES `moma-dw.moma_apps_staging.carts`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.payment_details`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.payment_details`
(
  id INT64 NOT NULL,
  uuid STRING(72),
  type STRING NOT NULL,
  status STRING NOT NULL,
  amount_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  properties JSON
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
