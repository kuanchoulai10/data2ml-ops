select
  src_account as src_account_id,
  dest_account as dest_account_id,
  amount,
  case
    when is_fraud = 1 then true
    when is_fraud = 0 then false
    else null
  end as is_fraud,
  timestamp as created_at
from {{ source('feast', 'transactions') }}
