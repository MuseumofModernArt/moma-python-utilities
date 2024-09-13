# moma-python-utilities
Python utilities and shared libraries to be used with gcp / ai projects

### pipelines

To run locally (there might be some requirements to install, you need to have gcloud installed with permission for gcp resources that are accessed):

```
python -m pip install -e .
```

```
  python -m moma.pipelines.synccarts \
    --runner direct \
    --jdbc-password-secret moma-apps-staging/secrets/sfdb-staging-password \
    --jdbc-username=u8dn62okb4cal2 \
    --jdbc-url=jdbc:postgresql://ec2-107-22-81-215.compute-1.amazonaws.com:5432/d5igktit12blu6 \
    --project moma-apps-staging \
    --temp-project moma-apps-staging \
    --destination-project moma-dw \
    --destination-dataset moma_apps_staging \
    --temp_location gs://pgsql-bq-loading-jobs/import-carts-dataflow/
```

    - or -

```
  python -m moma.pipelines.__init__ \
    --runner direct \
    --jdbc-password-secret moma-apps-staging/secrets/sfdb-staging-password \
    --jdbc-username=u8dn62okb4cal2 \
    --jdbc-url=jdbc:postgresql://ec2-107-22-81-215.compute-1.amazonaws.com:5432/d5igktit12blu6 \
    --project moma-apps-staging \
    --temp-project moma-apps-staging \
    --destination-project moma-dw \
    --destination-dataset moma_apps_staging \
    --temp_location gs://pgsql-bq-loading-jobs/import-carts-dataflow/ \
    --pipeline=carts
```

To run on gcp:

```
  python -m moma.pipelines.__init__ \
    --pipeline=carts \
    --runner DataflowRunner \
    --jdbc-password-secret moma-apps-staging/secrets/sfdb-staging-password \
    --jdbc-username=u8dn62okb4cal2 \
    --jdbc-url=jdbc:postgresql://ec2-107-22-81-215.compute-1.amazonaws.com:5432/d5igktit12blu6 \
    --project moma-apps-staging \
    --temp-project moma-apps-staging \
    --destination-project moma-dw \
    --destination-dataset moma_apps_staging \
    --region us-east4 \
    --no_use_public_ips \
    --network moma-apps-staging-vpc1 \
    --subnetwork https://www.googleapis.com/compute/v1/projects/moma-apps-staging/regions/us-east4/subnetworks/moma-apps-staging-vpc-us-east4 \
    --temp_location gs://pgsql-bq-loading-jobs/import-carts-dataflow/ \
    --experiments=use_runner_v2 \
    --staging_location gs://pgsql-bq-loading-jobs/staging/
```