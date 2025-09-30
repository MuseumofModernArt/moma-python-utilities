--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.virtual_queue_participants`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.virtual_queue_participants`
(
  id INT64 NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone_number STRING,
  phone_country_code STRING,
  virtual_queue_id INT64,
  slots INT64,
  status STRING,
  priority INT64,
  uuid STRING(72),
  marketing_opt_in BOOL,
  user_id INT64,
  web_push_device_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  receive_sms BOOL,
  notified_at TIMESTAMP,
  visiting_at TIMESTAMP,
  admitted_count INT64,
  cancelled_at TIMESTAMP,
  unserved_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (virtual_queue_id) REFERENCES `moma-dw.moma_apps.virtual_queues`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE `moma-membership.moma_import.virtual_queue_participants`
CREATE OR REPLACE TABLE `moma-membership.moma_import.virtual_queue_participants`
(
  id INT64 NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone_number STRING,
  phone_country_code STRING,
  virtual_queue_id INT64,
  slots INT64,
  status STRING,
  priority INT64,
  uuid STRING(72),
  marketing_opt_in BOOL,
  user_id INT64,
  web_push_device_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  receive_sms BOOL,
  notified_at TIMESTAMP,
  visiting_at TIMESTAMP,
  admitted_count INT64,
  cancelled_at TIMESTAMP,
  unserved_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (virtual_queue_id) REFERENCES `moma-membership.moma_import.virtual_queues`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.virtual_queue_participants`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.virtual_queue_participants`
(
  id INT64 NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone_number STRING,
  phone_country_code STRING,
  virtual_queue_id INT64,
  slots INT64,
  status STRING,
  priority INT64,
  uuid STRING(72),
  marketing_opt_in BOOL,
  user_id INT64,
  web_push_device_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  receive_sms BOOL,
  notified_at TIMESTAMP,
  visiting_at TIMESTAMP,
  admitted_count INT64,
  cancelled_at TIMESTAMP,
  unserved_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (virtual_queue_id) REFERENCES `moma-dw.moma_apps_staging.virtual_queues`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE `moma-apps-staging.moma_import.virtual_queue_participants`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.virtual_queue_participants`
(
  id INT64 NOT NULL,
  first_name STRING,
  last_name STRING,
  email STRING,
  phone_number STRING,
  phone_country_code STRING,
  virtual_queue_id INT64,
  slots INT64,
  status STRING,
  priority INT64,
  uuid STRING(72),
  marketing_opt_in BOOL,
  user_id INT64,
  web_push_device_id INT64,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  receive_sms BOOL,
  notified_at TIMESTAMP,
  visiting_at TIMESTAMP,
  admitted_count INT64,
  cancelled_at TIMESTAMP,
  unserved_at TIMESTAMP,
  properties JSON,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (virtual_queue_id) REFERENCES `moma-apps-staging.moma_import.virtual_queues`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);