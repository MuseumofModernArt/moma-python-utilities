--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.line_items`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.line_items`
(
  id INT64 NOT NULL,
  type STRING NOT NULL,
  quantity INT64,
  amount_in_cents INT64,
  discounted_total_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  finalized TIMESTAMP,
  properties JSON,
  delivery_properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (cart_id) REFERENCES `moma-dw.moma_apps.carts`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.line_items`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.line_items`
(
  id INT64 NOT NULL,
  type STRING NOT NULL,
  quantity INT64,
  amount_in_cents INT64,
  discounted_total_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  finalized TIMESTAMP,
  properties JSON,
  delivery_properties JSON
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.line_items`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.line_items`
(
  id INT64 NOT NULL,
  type STRING NOT NULL,
  quantity INT64,
  amount_in_cents INT64,
  discounted_total_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  finalized TIMESTAMP,
  properties JSON,
  delivery_properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (cart_id) REFERENCES `moma-dw.moma_apps_staging.carts`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.line_items`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.line_items`
(
  id INT64 NOT NULL,
  type STRING NOT NULL,
  quantity INT64,
  amount_in_cents INT64,
  discounted_total_in_cents INT64,
  cart_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  finalized TIMESTAMP,
  properties JSON,
  delivery_properties JSON
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);