from datetime import timedelta
from feast import BigQuerySource, FeatureView, Entity, ValueType

# Add an entity for users
user_entity = Entity(
    name="user_id",
    description="A user that has executed a transaction or received a transaction",
    value_type=ValueType.STRING
)

# Add a FeatureView based on our new table
driver_stats_fv = FeatureView(
    name="user_transaction_count_7d",
    entities=[user_entity],
    ttl=timedelta(weeks=1),
    source=BigQuerySource(
        table=f"mlops-437709.feast.user_count_transactions_7d",
        timestamp_field="feature_timestamp"
    )
)

# Add two FeatureViews based on existing tables in BigQuery
user_account_fv = FeatureView(
    name="user_account_features",
    entities=[user_entity],
    ttl=timedelta(weeks=52),
    source=BigQuerySource(
        table=f"feast-oss.fraud_tutorial.user_account_features",
        timestamp_field="feature_timestamp"
    )
)

user_has_fraudulent_transactions_fv = FeatureView(
    name="user_has_fraudulent_transactions",
    entities=[user_entity],
    ttl=timedelta(weeks=52),
    source=BigQuerySource(
        table=f"feast-oss.fraud_tutorial.user_has_fraudulent_transactions",
        timestamp_field="feature_timestamp"
    )
)
