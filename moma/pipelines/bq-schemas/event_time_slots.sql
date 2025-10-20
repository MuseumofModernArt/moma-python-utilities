CREATE TABLE `moma-dw.moma_apps.event_time_slots` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    max_quantity INT64,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    member_only boolean DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

CREATE TABLE `moma-dw.moma_apps_staging.event_time_slots` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    max_quantity INT64,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    member_only boolean DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.event_time_slots` (
    id INT64 NOT NULL,
    event_id INT64 NOT NULL,
    max_quantity INT64,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    member_only boolean DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
);

PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

