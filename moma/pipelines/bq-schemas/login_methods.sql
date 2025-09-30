--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.login_methods`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.login_methods`
(
  id INT64 NOT NULL,
  oauth_token STRING,
  auth0_reference STRING,
  user_id INT64 NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (user_id) REFERENCES `moma-dw.moma_apps.users`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.login_methods`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.login_methods`
(
  id INT64 NOT NULL,
  oauth_token STRING,
  auth0_reference STRING,
  user_id INT64 NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.login_methods`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.login_methods`
(
  id INT64 NOT NULL,
  oauth_token STRING,
  auth0_reference STRING,
  user_id INT64 NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED,
  FOREIGN KEY (user_id) REFERENCES `moma-dw.moma_apps_staging.users`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.login_methods`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.login_methods`
(
  id INT64 NOT NULL,
  oauth_token STRING,
  auth0_reference STRING,
  user_id INT64 NOT NULL,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);