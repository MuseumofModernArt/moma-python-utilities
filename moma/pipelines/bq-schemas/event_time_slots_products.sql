CREATE TABLE public.event_time_slots_products (
    id INT64 NOT NULL,
    event_time_slot_id INT64 NOT NULL,
    product_sfid STRING NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (event_time_slot_id) REFERENCES `moma-dw.moma_apps.event_time_slot`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);



