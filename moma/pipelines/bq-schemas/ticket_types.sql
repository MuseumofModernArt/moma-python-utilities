CREATE TABLE `moma-dw.moma_apps.ticket_types` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    caption STRING,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    ticket_identifier STRING NOT NULL,
    visible BOOL DEFAULT true NOT NULL,
    comp BOOL DEFAULT false NOT NULL,
    prior_days_can_sell_tickets INT64,
    event_user_max_quantity INT64,
    adult_ticket BOOL DEFAULT true NOT NULL,
    require_adult_ticket BOOL DEFAULT false NOT NULL,
    member_ticket BOOL DEFAULT false NOT NULL,
    require_member_ticket BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    internal_name STRING,
    ticket_type_category_id INT64,
    tax_deductible_amount_in_cents INT64 DEFAULT 0 NOT NULL,
    general_ledger_account STRING,
    general_ledger_designation STRING,
    require_child_ticket BOOL DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_category_id) REFERENCES `moma-dw.moma_apps.ticket_type_category`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-membership.moma_import.ticket_types` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    caption STRING,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    ticket_identifier STRING NOT NULL,
    visible BOOL DEFAULT true NOT NULL,
    comp BOOL DEFAULT false NOT NULL,
    prior_days_can_sell_tickets INT64,
    event_user_max_quantity INT64,
    adult_ticket BOOL DEFAULT true NOT NULL,
    require_adult_ticket BOOL DEFAULT false NOT NULL,
    member_ticket BOOL DEFAULT false NOT NULL,
    require_member_ticket BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    internal_name STRING,
    ticket_type_category_id INT64,
    tax_deductible_amount_in_cents INT64 DEFAULT 0 NOT NULL,
    general_ledger_account STRING,
    general_ledger_designation STRING,
    require_child_ticket BOOL DEFAULT false NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-dw.moma_apps_staging.ticket_types` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    caption STRING,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    ticket_identifier STRING NOT NULL,
    visible BOOL DEFAULT true NOT NULL,
    comp BOOL DEFAULT false NOT NULL,
    prior_days_can_sell_tickets INT64,
    event_user_max_quantity INT64,
    adult_ticket BOOL DEFAULT true NOT NULL,
    require_adult_ticket BOOL DEFAULT false NOT NULL,
    member_ticket BOOL DEFAULT false NOT NULL,
    require_member_ticket BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    internal_name STRING,
    ticket_type_category_id INT64,
    tax_deductible_amount_in_cents INT64 DEFAULT 0 NOT NULL,
    general_ledger_account STRING,
    general_ledger_designation STRING,
    require_child_ticket BOOL DEFAULT false NOT NULL,
    PRIMARY KEY (id) NOT ENFORCED,
    FOREIGN KEY (ticket_type_category_id) REFERENCES `moma-dw.moma_apps_staging.ticket_type_category`(id) NOT ENFORCED
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);


CREATE TABLE `moma-apps-staging.moma_import.ticket_types` (
    id INT64 NOT NULL,
    name STRING NOT NULL,
    caption STRING,
    price_in_cents INT64 DEFAULT 0 NOT NULL,
    ticket_identifier STRING NOT NULL,
    visible BOOL DEFAULT true NOT NULL,
    comp BOOL DEFAULT false NOT NULL,
    prior_days_can_sell_tickets INT64,
    event_user_max_quantity INT64,
    adult_ticket BOOL DEFAULT true NOT NULL,
    require_adult_ticket BOOL DEFAULT false NOT NULL,
    member_ticket BOOL DEFAULT false NOT NULL,
    require_member_ticket BOOL DEFAULT false NOT NULL,
    care_partner BOOL DEFAULT false NOT NULL,
    permit_care_partner BOOL DEFAULT false NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    internal_name STRING,
    ticket_type_category_id INT64,
    tax_deductible_amount_in_cents INT64 DEFAULT 0 NOT NULL,
    general_ledger_account STRING,
    general_ledger_designation STRING,
    require_child_ticket BOOL DEFAULT false NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(created_at, MONTH) OPTIONS (require_partition_filter = TRUE);

