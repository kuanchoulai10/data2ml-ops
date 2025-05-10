select
  user_id as account_id,
  case
    when user_has_fraudulent_transactions_7d = 1 then true
    when user_has_fraudulent_transactions_7d = 0 then false
    else null
  end as has_fraud_7d,
  feature_timestamp
from {{ source('feast', 'user_has_fraudulent_transactions') }}
