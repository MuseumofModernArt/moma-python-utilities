CREATE TABLE `moma-dw.moma_apps.ticket_bucket_tickets` (
    id INT64 NOT NULL,
    bucket_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    name_override STRING,
    caption STRING,
    position INT64 DEFAULT 0 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    admission_value STRING DEFAULT 'full' NOT NULL,
    child_ticket BOOL DEFAULT false NOT NULL,
    disables_upsell BOOL DEFAULT false NOT NULL,
    adult BOOL DEFAULT true NOT NULL,
    require_adult BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    member BOOL DEFAULT false NOT NULL,
    require_member BOOL DEFAULT false NOT NULL,
    staff BOOL DEFAULT false NOT NULL,
    require_staff BOOL DEFAULT false NOT NULL,
    student_ticket BOOL DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-membership.moma_import.ticket_bucket_tickets` (
    id INT64 NOT NULL,
    bucket_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    name_override STRING,
    caption STRING,
    position INT64 DEFAULT 0 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    admission_value STRING DEFAULT 'full' NOT NULL,
    child_ticket BOOL DEFAULT false NOT NULL,
    disables_upsell BOOL DEFAULT false NOT NULL,
    adult BOOL DEFAULT true NOT NULL,
    require_adult BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    member BOOL DEFAULT false NOT NULL,
    require_member BOOL DEFAULT false NOT NULL,
    staff BOOL DEFAULT false NOT NULL,
    require_staff BOOL DEFAULT false NOT NULL,
    student_ticket BOOL DEFAULT false NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.ticket_bucket_tickets` (
    id INT64 NOT NULL,
    bucket_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    name_override STRING,
    caption STRING,
    position INT64 DEFAULT 0 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    admission_value STRING DEFAULT 'full' NOT NULL,
    child_ticket BOOL DEFAULT false NOT NULL,
    disables_upsell BOOL DEFAULT false NOT NULL,
    adult BOOL DEFAULT true NOT NULL,
    require_adult BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    member BOOL DEFAULT false NOT NULL,
    require_member BOOL DEFAULT false NOT NULL,
    staff BOOL DEFAULT false NOT NULL,
    require_staff BOOL DEFAULT false NOT NULL,
    student_ticket BOOL DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.ticket_bucket_tickets` (
    id INT64 NOT NULL,
    bucket_name STRING NOT NULL,
    product_sfid STRING NOT NULL,
    name_override STRING,
    caption STRING,
    position INT64 DEFAULT 0 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    admission_value STRING DEFAULT 'full' NOT NULL,
    child_ticket BOOL DEFAULT false NOT NULL,
    disables_upsell BOOL DEFAULT false NOT NULL,
    adult BOOL DEFAULT true NOT NULL,
    require_adult BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    member BOOL DEFAULT false NOT NULL,
    require_member BOOL DEFAULT false NOT NULL,
    staff BOOL DEFAULT false NOT NULL,
    require_staff BOOL DEFAULT false NOT NULL,
    student_ticket BOOL DEFAULT false NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);
