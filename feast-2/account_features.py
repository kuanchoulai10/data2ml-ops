from datetime import timedelta

from feast import (BigQuerySource, Entity, FeatureService, FeatureView,
                   ValueType, Field)
from feast.types import STRING, INT64, BOOL

# Data Sources
# https://rtd.feast.dev/en/latest/index.html#feast.infra.offline_stores.bigquery_source.BigQuerySource
ds_acct_fraud_7d = BigQuerySource(
    table=f"mlops-437709.dbt_kclai.feat_acct_fraud_7d",
    timestamp_field="feature_timestamp"
)

ds_acct_num_txns_7d = BigQuerySource(
    table=f"mlops-437709.dbt_kclai.feat_acct_num_txns_7d",
    timestamp_field="feature_timestamp"
)

ds_acct_profiles = BigQuerySource(
    table=f"mlops-437709.dbt_kclai.feat_acct_profiles",
    timestamp_field="feature_timestamp"
)

# Entity
account_entity = Entity(
    name="Account",
    description="A user that has executed a transaction or received a transaction",
    value_type=ValueType.STRING,
    join_keys=["entity_id"]
)

# Feature Views
fv_acct_fraud_7d = FeatureView(
    name="acct_fraud_7d",
    entities=[account_entity],
    schema=[
        Field(name="has_fraud_7d", dtype=BOOL)
    ],
    ttl=timedelta(weeks=52),
    source=ds_acct_fraud_7d
)


fv_acct_num_txns_7d = FeatureView(
    name="acct_num_txns_7d",
    entities=[account_entity],
    schema=[
        Field(name="num_transactions_7d", dtype=INT64)
    ],
    ttl=timedelta(weeks=1),
    source=ds_acct_num_txns_7d
)

fv_acct_profiles = FeatureView(
    name="acct_profiles",
    entities=[account_entity],
    schema=[
        Field(name="credit_score", dtype=INT64),
        Field(name="account_age_days", dtype=INT64),
        Field(name="has_2fa_installed", dtype=BOOL)
    ],
    ttl=timedelta(weeks=52),
    source=ds_acct_profiles
)



# Feature Services
# Versioning features that power ML models:
# https://docs.feast.dev/master/how-to-guides/running-feast-in-production#id-3.2-versioning-features-that-power-ml-models
fs_fraud_detection_v1 = FeatureService(
    name="fraud_detection_v1",
    features=[
        fv_acct_fraud_7d,
        fv_acct_num_txns_7d[["num_transactions_7d"]],
        fv_acct_profiles
    ]
)