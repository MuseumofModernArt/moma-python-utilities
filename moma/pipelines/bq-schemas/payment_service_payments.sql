-- PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.payment_service_payments`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.payment_service_payments`
(
  id STRING(72) NOT NULL,
  amount INT64,
  external_reference STRING,
  currency STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  status STRING,
  terminal_id STRING,
  last_digits STRING,
  card_token STRING,
  shopper_reference STRING,
  card_brand STRING,
  amount_in_cents integer,
  first_name STRING,
  last_name STRING,
  email STRING,
  ip_address STRING,
  additional_risk_data JSON,
  raw_payment_data JSON,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.payment_service_payments`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.payment_service_payments`
(
  id STRING(72) NOT NULL,
  amount INT64,
  external_reference STRING,
  currency STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  status STRING,
  terminal_id STRING,
  last_digits STRING,
  card_token STRING,
  shopper_reference STRING,
  card_brand STRING,
  amount_in_cents integer,
  first_name STRING,
  last_name STRING,
  email STRING,
  ip_address STRING,
  additional_risk_data JSON,
  raw_payment_data JSON,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.payment_service_payments`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.payment_service_payments`
(
  id STRING(72) NOT NULL,
  amount INT64,
  external_reference STRING,
  currency STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  status STRING,
  terminal_id STRING,
  last_digits STRING,
  card_token STRING,
  shopper_reference STRING,
  card_brand STRING,
  amount_in_cents integer,
  first_name STRING,
  last_name STRING,
  email STRING,
  ip_address STRING,
  additional_risk_data JSON,
  raw_payment_data JSON,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.payment_service_payments`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.payment_service_payments`
(
  id STRING(72) NOT NULL,
  amount INT64,
  external_reference STRING,
  currency STRING,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  status STRING,
  terminal_id STRING,
  last_digits STRING,
  card_token STRING,
  shopper_reference STRING,
  card_brand STRING,
  amount_in_cents integer,
  first_name STRING,
  last_name STRING,
  email STRING,
  ip_address STRING,
  additional_risk_data JSON,
  raw_payment_data JSON,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);