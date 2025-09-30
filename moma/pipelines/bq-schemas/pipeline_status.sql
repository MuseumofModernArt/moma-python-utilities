-- PRODUCTION moma_import

-- DROP TABLE IF EXISTS `moma-membership.moma_import.pipeline_status`;
CREATE OR REPLACE TABLE `moma-membership.moma_import.pipeline_status`
(
  name STRING NOT NULL,
  uuid STRING NOT NULL,
  status STRING NOT NULL,
  began_at TIMESTAMP NOT NULL
);

-- STAGING moma_import

-- DROP TABLE IF EXISTS `moma-apps-staging.moma_import.pipeline_status`;
CREATE OR REPLACE TABLE `moma-apps-staging.moma_import.pipeline_status`
(
  name STRING NOT NULL,
  uuid STRING NOT NULL,
  status STRING NOT NULL,
  began_at TIMESTAMP NOT NULL
);