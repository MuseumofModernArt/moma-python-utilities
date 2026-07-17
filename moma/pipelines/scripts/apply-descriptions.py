#!/usr/bin/env python3
"""Apply table & column descriptions to the destination BigQuery tables.

Descriptions live in ``moma/pipelines/descriptions/<bq_table_name>.yaml`` (one file per
synced table). This script pushes them into the ``description`` metadata of the permanent
destination tables that analysts / AI query:

    staging     -> moma-dw.moma_apps_staging.<table>
    production  -> moma-dw.moma_apps.<table>

It is **non-destructive**: it only updates the table-level and column-level ``description``
fields via ``Client.update_table(table, ["description", "schema"])``. It never creates,
drops, truncates, or repartitions a table and never touches row data. The transient
``moma_import.*`` staging tables are intentionally not targeted.

Usage
-----
    # Validate the YAML against the sync modules' Record fields (no credentials needed):
    python moma/pipelines/scripts/apply-descriptions.py --check

    # Preview what would be applied to an environment (reads live schema, writes nothing):
    python moma/pipelines/scripts/apply-descriptions.py --env staging --dry-run

    # Apply for real (staging first, then production after review):
    python moma/pipelines/scripts/apply-descriptions.py --env staging
    python moma/pipelines/scripts/apply-descriptions.py --env production

``--env`` requires ``gcloud`` application-default credentials with BigQuery write access to
the ``moma-dw`` datasets. ``--check`` runs fully locally (only needs PyYAML).
"""

import argparse
import ast
import glob
import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(HERE)                     # .../moma/pipelines
DESCRIPTIONS_DIR = os.path.join(PIPELINES_DIR, 'descriptions')

# env -> (project, dataset) of the permanent destination tables analysts query.
ENV_DATASETS = {
    'staging': ('moma-dw', 'moma_apps_staging'),
    'production': ('moma-dw', 'moma_apps'),
}

# BigQuery hard limit on a column/field description.
MAX_COLUMN_DESCRIPTION = 1024


def load_descriptions():
    """Read every descriptions/*.yaml -> {table: {'table': str, 'columns': {col: str}}}."""
    out = {}
    for path in sorted(glob.glob(os.path.join(DESCRIPTIONS_DIR, '*.yaml'))):
        table = os.path.splitext(os.path.basename(path))[0]
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        table_desc = (data.get('table') or '').strip()
        columns = data.get('columns') or {}
        columns = {k: (v or '').strip() for k, v in columns.items()}
        out[table] = {'table': table_desc, 'columns': columns}
    return out


def sync_record_fields():
    """Map bq_table_name -> ordered Record field names by AST-parsing the sync modules.

    Parsing (rather than importing) keeps this dependency-free and credential-free:
    importing ``moma.pipelines`` would instantiate a Secret Manager client and pull in
    apache-beam, neither of which is available or wanted for a local ``--check``.
    """
    mapping = {}
    for path in sorted(glob.glob(os.path.join(PIPELINES_DIR, 'sync*.py'))):
        with open(path) as f:
            tree = ast.parse(f.read(), filename=path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            bq_name = None
            fields = None
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if (isinstance(target, ast.Name)
                                and target.id == 'bq_table_name'
                                and isinstance(item.value, ast.Constant)):
                            bq_name = item.value.value
                if isinstance(item, ast.ClassDef) and item.name == 'Record':
                    fields = [b.target.id for b in item.body
                              if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name)]
            if bq_name and fields is not None:
                mapping[bq_name] = fields
    return mapping


def check():
    """Validate the YAML dictionary against the sync modules. Returns an exit code."""
    descs = load_descriptions()
    fields = sync_record_fields()
    problems = 0

    missing_yaml = sorted(set(fields) - set(descs))
    for table in missing_yaml:
        print(f'MISSING: no descriptions/{table}.yaml for synced table "{table}"')
        problems += 1

    orphan_yaml = sorted(set(descs) - set(fields))
    for table in orphan_yaml:
        print(f'ORPHAN:  descriptions/{table}.yaml has no matching sync module')
        problems += 1

    for table in sorted(set(descs) & set(fields)):
        record_cols = fields[table]
        yaml_cols = descs[table]['columns']
        if not descs[table]['table']:
            print(f'{table}: table-level description is empty')
            problems += 1
        missing = [c for c in record_cols if c not in yaml_cols]
        extra = [c for c in yaml_cols if c not in record_cols]
        if missing:
            print(f'{table}: columns missing a description: {", ".join(missing)}')
            problems += 1
        if extra:
            print(f'{table}: YAML columns not in Record: {", ".join(extra)}')
            problems += 1
        for col, text in yaml_cols.items():
            if not text:
                print(f'{table}.{col}: empty description')
                problems += 1
            elif len(text) > MAX_COLUMN_DESCRIPTION:
                print(f'{table}.{col}: description is {len(text)} chars (>{MAX_COLUMN_DESCRIPTION} limit)')
                problems += 1

    if problems:
        print(f'\n{problems} problem(s) found across {len(descs)} description file(s).')
        return 1
    print(f'OK: {len(descs)} description files validate against {len(fields)} sync modules.')
    return 0


def apply(env, dry_run):
    """Apply (or preview) descriptions to the destination tables for one environment."""
    from google.cloud import bigquery  # lazy: only needed when talking to BigQuery

    project, dataset = ENV_DATASETS[env]
    client = bigquery.Client(project=project)
    descs = load_descriptions()
    verb = 'Would update' if dry_run else 'Updating'
    updated = 0

    for table in sorted(descs):
        fqn = f'{project}.{dataset}.{table}'
        try:
            tbl = client.get_table(fqn)
        except Exception as exc:  # noqa: BLE001 - report and continue past missing tables
            print(f'SKIP {fqn}: {exc}')
            continue

        col_desc = descs[table]['columns']
        live_cols = {f.name for f in tbl.schema}
        for col in col_desc:
            if col not in live_cols:
                print(f'WARN {fqn}: YAML column "{col}" not present in the live table')
        for col in live_cols:
            if col not in col_desc:
                print(f'WARN {fqn}: live column "{col}" has no YAML description')

        new_schema = []
        for field in tbl.schema:
            repr_ = field.to_api_repr()
            if col_desc.get(field.name):
                repr_['description'] = col_desc[field.name]
            new_schema.append(bigquery.SchemaField.from_api_repr(repr_))

        tbl.schema = new_schema
        tbl.description = descs[table]['table']

        print(f'{verb} {fqn} (table + {len(col_desc)} columns)')
        if not dry_run:
            client.update_table(tbl, ['description', 'schema'])
        updated += 1

    print(f'\n{verb.split()[0]} {updated} table(s) in {project}.{dataset}.')
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--env', choices=sorted(ENV_DATASETS),
                        help='destination environment to apply descriptions to')
    parser.add_argument('--dry-run', action='store_true',
                        help='with --env: read live schema and print changes without writing')
    parser.add_argument('--check', action='store_true',
                        help='validate YAML against sync modules locally (no BigQuery)')
    args = parser.parse_args(argv)

    if args.check or not args.env:
        return check()
    return apply(args.env, args.dry_run)


if __name__ == '__main__':
    sys.exit(main())
