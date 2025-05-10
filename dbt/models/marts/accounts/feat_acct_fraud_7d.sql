select
  account_id as entity_id,
  has_fraud_7d,
  feature_timestamp
from {{ ref('fraud', 'stg__feast__acct_fraud_7d') }}
