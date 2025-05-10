select
  account_id as entity_id,
  num_transactions_7d,
  cast(transaction_date as timestamp) as feature_timestamp
from {{ ref("fraud", "int__feast__acct_num_txns__extented") }}
