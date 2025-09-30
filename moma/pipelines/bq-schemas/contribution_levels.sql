-- PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.contribution_levels`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.contribution_levels`
(
  id INT64 NOT NULL,
  special_event_id INT64,
  name STRING,
  caption STRING,
  dollar_amount INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  quantity_limit INT64,
  tax_deductible_dollar_amount INT64,
  ticket_identifier STRING,
  visible BOOL,
  number_of_guests INT64,
  display_order INT64,
  order_quantity_limit INT64,
  comp BOOL,
  concierge_ticket BOOL,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.contribution_levels`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.contribution_levels`
(
  id INT64 NOT NULL,
  special_event_id INT64,
  name STRING,
  caption STRING,
  dollar_amount INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  quantity_limit INT64,
  tax_deductible_dollar_amount INT64,
  ticket_identifier STRING,
  visible BOOL,
  number_of_guests INT64,
  display_order INT64,
  order_quantity_limit INT64,
  comp BOOL,
  concierge_ticket BOOL,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.contribution_levels`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.contribution_levels`
(
  id INT64 NOT NULL,
  special_event_id INT64,
  name STRING,
  caption STRING,
  dollar_amount INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  quantity_limit INT64,
  tax_deductible_dollar_amount INT64,
  ticket_identifier STRING,
  visible BOOL,
  number_of_guests INT64,
  display_order INT64,
  order_quantity_limit INT64,
  comp BOOL,
  concierge_ticket BOOL,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.contribution_levels`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.contribution_levels`
(
  id INT64 NOT NULL,
  special_event_id INT64,
  name STRING,
  caption STRING,
  dollar_amount INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  quantity_limit INT64,
  tax_deductible_dollar_amount INT64,
  ticket_identifier STRING,
  visible BOOL,
  number_of_guests INT64,
  display_order INT64,
  order_quantity_limit INT64,
  comp BOOL,
  concierge_ticket BOOL,
  PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);