CREATE TABLE `moma-dw.moma_apps.price_lists` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    description STRING varying,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.price_lists` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    description STRING varying,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.price_lists` (
    id INT64 NOT NULL,
    name STRING varying NOT NULL,
    description STRING varying,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


