--PRODUCTION destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps.admin_users`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps.admin_users`
(
  id INT64 NOT NULL,
  email STRING NOT NULL,
  google_id STRING,
  created_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
);

-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.admin_users`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.admin_users`
(
  id INT64 NOT NULL,
  email STRING NOT NULL,
  google_id STRING,
  created_at TIMESTAMP
);

-- STAGING destination tables

-- DROP TABLE IF EXISTS `moma-dw.moma_apps_staging.admin_users`;
CREATE OR REPLACE TABLE `moma-dw.moma_apps_staging.admin_users`
(
  id INT64 NOT NULL,
  email STRING NOT NULL,
  google_id STRING,
  created_at TIMESTAMP,
  PRIMARY KEY (id) NOT ENFORCED
);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.admin_users`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.admin_users`
(
  id INT64 NOT NULL,
  email STRING NOT NULL,
  google_id STRING,
  created_at TIMESTAMP
);