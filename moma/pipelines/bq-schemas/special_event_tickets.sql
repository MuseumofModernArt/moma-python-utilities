--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.special_event_tickets`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.special_event_tickets`
(
  id INT64 NOT NULL,
  name STRING,
  dollar_amount INT64,
  identifier STRING,
  status STRING,
  contribution_level_id INT64,
  line_item_id INT64,
  special_event_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (line_item_id) REFERENCES `moma-dw.moma_apps.line_items`(id) NOT ENFORCED,
  FOREIGN KEY (special_event_id) REFERENCES `moma-dw.moma_apps.special_events`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.special_event_tickets`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.special_event_tickets`
(
  id INT64 NOT NULL,
  name STRING,
  dollar_amount INT64,
  identifier STRING,
  status STRING,
  contribution_level_id INT64,
  line_item_id INT64,
  special_event_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.special_event_tickets`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.special_event_tickets`
(
  id INT64 NOT NULL,
  name STRING,
  dollar_amount INT64,
  identifier STRING,
  status STRING,
  contribution_level_id INT64,
  line_item_id INT64,
  special_event_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (line_item_id) REFERENCES `moma-dw.moma_apps_staging.line_items`(id) NOT ENFORCED,
  FOREIGN KEY (special_event_id) REFERENCES `moma-dw.moma_apps_staging.special_events`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.special_event_tickets`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.special_event_tickets`
(
  id INT64 NOT NULL,
  name STRING,
  dollar_amount INT64,
  identifier STRING,
  status STRING,
  contribution_level_id INT64,
  line_item_id INT64,
  special_event_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);