# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`moma` is a Python package of shared utilities for MoMA's GCP / AI projects. Python 3.12 (`.tool-versions` pins 3.12.1). The repo uses a `.venv` (auto-activated via `.autoenv`).

Install for local development (editable):

```
python -m pip install -e .
```

There is no test suite, linter, or build step configured in the repo — dependencies are listed in `requirements.txt` and packaging metadata in `pyproject.toml`.

## Three independent modules

- **`moma/pipelines/`** — Apache Beam ETL that syncs tables from a Postgres (Salesforce app DB) source into BigQuery, runnable locally (`--runner direct`) or on Cloud Dataflow (`--runner DataflowRunner`). This is the bulk of the codebase.
- **`moma/ai/`** — thin wrappers over `anthropic`, `openai`, and `vertexai` SDKs for image-description / LLM calls. Note `moma/ai/anthropic.py` defaults to an old model id (`claude-3-opus-20240229`) and reads the key from env var `ANTHROPIC_API_KEY_ENV`.
- **`moma/typer/`** — a Typer CLI (`cloud_functions.py`) for local development of GCP Cloud Functions: runs the Pub/Sub emulator, builds buildpack images, deploys gen2 functions, publishes test messages. It reads function definitions from a sibling project's `.vscode/launch.json` (`cloudcode.cloudfunctions` entries), so it is meant to be run from within a cloud-functions repo, not this one.

## Pipelines architecture

These pipelines sync tables from the SFDB Postgres database (which drives membership.moma.org) into the BigQuery data warehouse `moma-dw`. The sync is **incremental and upsert-only**: it reads source rows changed since the last successful run's watermark, stages them, then `MERGE`s into the destination over the source's `created_at` partition window — matched rows are updated, new rows inserted, and **rows are never deleted** from the destination.

Every table has a `sync<tablename>.py` module defining a single model class (e.g. `Cart`, `User`) with a fixed shape. `moma/pipelines/__init__.py` is the shared engine and dispatcher.

A model class must define:
- `Record(typing.NamedTuple)` — the column shape; `Record._fields` drives the BigQuery MERGE.
- `name` — CamelCase label used in Beam transform names.
- `job_name` — key used in the `pipeline_status` table for incremental-sync bookkeeping (e.g. `import-carts`).
- `bq_table_name` / `pg_table_name` — BigQuery and Postgres table names.
- `bq_table_schema` — `{'fields': [...]}` BigQuery schema dicts.
- `pg_source_query(begin, end)` — parameterized SQL. Timestamps are formatted in Postgres via `to_char(... 'YYYY-MM-DD HH24:MI:SS"."US')`; the incremental filter uses `WHERE updated_at >= '{begin}'`.
- `to_dict(row)` — usually `row._asdict()`.
- `run = pl.make_runner(<ModelClass>)` at module bottom.

`make_runner` (in `__init__.py`) implements the run flow:
1. Look up the last successful run in `<temp_project>.moma_import.pipeline_status`; the sync window is `[last_success.began_at - 5min, now]` (5-minute overlap guards against missed rows).
2. Read from Postgres via `ReadFromJdbc` (postgres JDBC driver), password fetched from Secret Manager (**hardcoded to `versions/2`** in `postgres_source`).
3. Write to the staging table `<temp_project>:moma_import.<table>` with `WRITE_TRUNCATE` / `CREATE_NEVER` (staging table must already exist).
4. `bigquery_merge` runs a `MERGE` from staging into `<dest_project>.<dest_dataset>.<table>` keyed on `id` + `created_at` partition window, then `TRUNCATE`s staging.
5. Update `pipeline_status` to `success`.

Because MERGE and status queries assume a `created_at` column and `id` key, new tables generally need both.

### Naming conventions

- Sync file: `sync<table_name>.py` with the table name downcased and all punctuation stripped (`payment_service.payments` → `syncpaymentservicepayments.py`).
- Class: singular table name in CamelCase (`PaymentServicePayment`, `ContributionLevel`).
- `job_name`: `import-<table-name>` with punctuation replaced by hyphens (`import-payment-service-payments`).
- Dispatch `case` key in `__init__.py`: the underscored table name (`payment_service_payments`).

### Adding a new table

1. **Schema files.** Add `moma/pipelines/bq-schemas/<table>.sql`. Each file holds **four `CREATE TABLE` statements**, one per environment target (see table below). These files are documentation only — they are **not run by any script**; you must run the DDL manually in BigQuery before deploying. Create referenced foreign-key tables first. (The `schema-getter.ipynb` notebook helps pull existing schemas.) Common Postgres→BigQuery type mappings: `varchar/char/text/uuid`→`STRING` (`uuid`→`STRING(72)`), `int/bigint`→`INT64`, `boolean`→`BOOL`, `time/date/datetime/timestamp`→`TIMESTAMP`, `jsonb`→`JSON`.
2. Generate `Record` and `bq_table_schema` boilerplate:
   ```
   python moma/pipelines/scripts/schema-maker.py <table>
   ```
   "Record Schema" fills `class Record(typing.NamedTuple)`; "Transfer Schema" fills `bq_table_schema['fields']`. (Note: `schema-maker.py`'s regex is hardcoded to the `moma-membership.moma_import` project and a `TYPE_CONVERSION` map that may need extending for new BQ types.) `bq_table_schema` mode is `REQUIRED` for `NOT NULL` columns, `NULLABLE` otherwise. Postgres→Python types: text/uuid→`str`, int/bigint→`int`, boolean→`bool`, time/date/timestamp→`datetime.datetime`, jsonb→`dict`, array→`list`.
3. Write `sync<table>.py` following an existing module like `synccarts.py`. The `pg_source_query` should end with `WHERE updated_at >= timestamp '{begin.isoformat()}';`.
4. Add the dispatch `case` to `__init__.py` (generate with `python moma/pipelines/scripts/case-maker.py <table>`), then verify the `make_runner(...)` argument matches the class name in the sync file.
5. Add `moma/pipelines/descriptions/<bq_table_name>.yaml` documenting the table and every column (see "Table & column descriptions" below).

### Type-casting conventions in pipelines

The JDBC/Beam round-trip needs several source-side casts, applied in `pg_source_query` and sometimes reversed in `to_dict`:

- **Booleans:** in `to_dict`, coerce with `d['active'] = d['active'] == 'true'` for each bool column; optionally `COALESCE` a default in SQL (`coalesce(optional_address::text, 'false') AS optional_address`).
- **`uuid` columns:** cast in SQL with `id::text AS id`.
- **Nullable timestamps:** NULLs must be replaced with a sentinel in SQL, then nulled again in `to_dict`:
  ```sql
  to_char(coalesce(last_authenticated_on, '3000-01-01'::timestamp), 'YYYY-MM-DD HH24:MI:SS"."US') as last_authenticated_on
  ```
  ```python
  if d['last_authenticated_on'] == '3000-01-01 00:00:00.000000':
      d['last_authenticated_on'] = None
  ```
- **Nullable `TIME` columns:** convert to TIMESTAMP/DATETIME first, then follow the timestamp pattern. See `syncevents.py` for a worked example.

### Adding a column to an existing table

Do **not** re-run the full schema file (it would drop data). Instead: add the column to the `.sql` file for reference, run `ALTER TABLE ... ADD COLUMN` on all four targets manually, and add the column to the sync file's `Record`, `bq_table_schema`, and `pg_source_query`. Before the first sync backfills the column, clear the pipeline's watermark so all rows re-sync:
```sql
DELETE FROM `<temp_project>.moma_import.pipeline_status` WHERE name = 'import-<table-name>'
```
(run against both `moma-apps-staging` and `moma-membership`). Also add the new column to
`moma/pipelines/descriptions/<table>.yaml`.

### Table & column descriptions (data dictionary)

BigQuery table/column `description` metadata for the destination tables is authored in a YAML
data dictionary and applied non-destructively — it exists so an AI/analyst querying the tables
has semantic context (what tables mean, enum/status vocabularies, money units, and how
primary/foreign keys join).

- **Source of truth:** `moma/pipelines/descriptions/<bq_table_name>.yaml`, one file per synced
  table, shaped as `table: <paragraph>` + `columns: {<col>: <text>}`. The file name and column
  keys must match the sync module's `bq_table_name` and `Record._fields` exactly. Descriptions
  are prose only — they carry no schema/type info and never affect the pipeline run.
- **Apply tool:** `moma/pipelines/scripts/apply-descriptions.py` pushes descriptions into the
  destination tables that analysts query (`moma-dw.moma_apps` and `moma-dw.moma_apps_staging`;
  the transient `moma_import.*` tables are intentionally skipped). It only updates `description`
  metadata via `Client.update_table(..., ["description", "schema"])` — it never creates, drops,
  truncates, or repartitions anything.
  - `--check` — validate the YAML against the sync modules (columns present, non-empty, within
    BigQuery's 1024-char column limit). Runs fully locally (only needs PyYAML); no credentials.
  - `--env staging|production --dry-run` — read the live schema and print what would change.
  - `--env staging` then, after review, `--env production` — apply for real (needs `gcloud`
    application-default credentials with BigQuery write access to `moma-dw`).
- **Workflow when adding/changing a column:** update the table's YAML, run `--check`, then apply
  per env. Descriptions are NOT set by the `bq-schemas/*.sql` DDL, so a `CREATE OR REPLACE` of a
  table drops them — re-run `apply-descriptions.py` for that env afterward.

## Environments and deployment

There are two environments, distinguished by the `--temp-project` / `--destination-project` / `--destination-dataset` flags:

| | staging | production |
|---|---|---|
| App / temp project | `moma-apps-staging` | `moma-membership` |
| Staging tables | `<temp_project>.moma_import.<table>` | same |
| Destination | `moma-dw.moma_apps_staging.<table>` | `moma-dw.moma_apps.<table>` |

This package is **consumed as a library** by the `moma-apps-gcp` repo, which runs the pipelines on Cloud Run (service `moma-apps-import-data-pipelines`) triggered hourly by Cloud Scheduler jobs (one per pipeline, staggered at 5-minute offsets, each POSTing `{"pipeline": "<name>"}`).

Release flow:
1. In this repo, commit, then tag the next version (`git ls-remote --tags origin` shows the latest): `git tag -f vX.Y && git push && git push origin vX.Y`.
2. In `moma-apps-gcp`, bump the pinned version in `cloudrun/importdatapipelines/requirements.txt` (`moma @ git+https://github.com/MuseumofModernArt/moma-python-utilities.git@vX.Y`), commit, push.
3. Run the Cloud Build trigger `deploy-moma-apps-import-data-pipeline` for staging (`moma-apps-staging`) first, then production (`moma-membership`); create/run the Cloud Scheduler job for the new pipeline. Verify in staging before deploying to production.

The full runbook — including one-time IAM / Cloud Build service-account setup, GitHub connection setup, and the exact `gcloud` scheduler/build/deploy commands per pipeline — lives at https://github.com/MuseumofModernArt/moma-engineering-documentation/blob/main/gcp/sfdb-to-moma-dw-pipelines.md.

### Running a pipeline locally

Select the pipeline with `--pipeline=<table>` (or the `PIPELINE` env var), or invoke the module directly. Local run:

```
python -m moma.pipelines.synccarts \
  --runner direct \
  --jdbc-password-secret <project>/secrets/<secret-name> \
  --jdbc-username=<user> \
  --jdbc-url=jdbc:postgresql://<host>:5432/<db> \
  --project <gcp-project> \
  --temp-project <gcp-project> \
  --destination-project moma-dw \
  --destination-dataset <dataset> \
  --temp_location gs://<bucket>/...
```

For Dataflow, use `--runner DataflowRunner` plus VPC/subnetwork/region flags (see `README.md` for the full example). Running requires `gcloud` installed and authenticated with access to the referenced GCP resources and secrets.
