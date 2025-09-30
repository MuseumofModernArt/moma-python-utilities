-- PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.ticketing_tickets`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.ticketing_tickets`
(
  id STRING(72) NOT NULL,
  ticket_type_id STRING NOT NULL,
  name STRING,
  description STRING,
  type_of_ticket STRING,
  price INT64 NOT NULL,
  ticket_number STRING,
  barcode STRING,
  date STRING,
  status INT64,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  external_order_item_id STRING,
  external_id STRING,
  event_id STRING,
  template_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-dw.moma_apps.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.ticketing_tickets`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.ticketing_tickets`
(
  id STRING(72) NOT NULL,
  ticket_type_id STRING NOT NULL,
  name STRING,
  description STRING,
  type_of_ticket STRING,
  price INT64 NOT NULL,
  ticket_number STRING,
  barcode STRING,
  date STRING,
  status INT64,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  external_order_item_id STRING,
  external_id STRING,
  event_id STRING,
  template_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-membership.moma_import.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.ticketing_tickets`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.ticketing_tickets`
(
  id STRING(72) NOT NULL,
  ticket_type_id STRING NOT NULL,
  name STRING,
  description STRING,
  type_of_ticket STRING,
  price INT64 NOT NULL,
  ticket_number STRING,
  barcode STRING,
  date STRING,
  status INT64,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  external_order_item_id STRING,
  external_id STRING,
  event_id STRING,
  template_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-dw.moma_apps_staging.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.ticketing_tickets`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.ticketing_tickets`
(
  id STRING(72) NOT NULL,
  ticket_type_id STRING NOT NULL,
  name STRING,
  description STRING,
  type_of_ticket STRING,
  price INT64 NOT NULL,
  ticket_number STRING,
  barcode STRING,
  date STRING,
  status INT64,
  order_id STRING(72) NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  external_order_item_id STRING,
  external_id STRING,
  event_id STRING,
  template_id STRING,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (order_id) REFERENCES `moma-apps-staging.moma_import.ticketing_orders`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);