--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.refunds`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.refunds`
(
  id STRING NOT NULL,
  payment_detail_id INT64,
  idempotency_key STRING,
  amount_in_cents INT64,
  status STRING,
  ticket_numbers JSON,
  line_items JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  additional_notes STRING,
  reason INT64,
  issued_by STRING,
  customer_email STRING,
  cc_email STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (payment_detail_id) REFERENCES `moma-dw.moma_apps.payment_details`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE `moma-membership.moma_import.refunds`
CREATE OR REPLACE TABLE `moma-membership.moma_import.refunds`
(
   id STRING NOT NULL,
  payment_detail_id INT64,
  idempotency_key STRING,
  amount_in_cents INT64,
  status STRING,
  ticket_numbers JSON,
  line_items JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  additional_notes STRING,
  reason INT64,
  issued_by STRING,
  customer_email STRING,
  cc_email STRING
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.refunds`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.refunds`
(
  id STRING NOT NULL,
  payment_detail_id INT64,
  idempotency_key STRING,
  amount_in_cents INT64,
  status STRING,
  ticket_numbers JSON,
  line_items JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  additional_notes STRING,
  reason INT64,
  issued_by STRING,
  customer_email STRING,
  cc_email STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (payment_detail_id) REFERENCES `moma-dw.moma_apps_staging.payment_details`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE `moma-apps-staging.moma_import.refunds`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.refunds`
(
  id STRING NOT NULL,
  payment_detail_id INT64,
  idempotency_key STRING,
  amount_in_cents INT64,
  status STRING,
  ticket_numbers JSON,
  line_items JSON,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  additional_notes STRING,
  reason INT64,
  issued_by STRING,
  customer_email STRING,
  cc_email STRING,
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);