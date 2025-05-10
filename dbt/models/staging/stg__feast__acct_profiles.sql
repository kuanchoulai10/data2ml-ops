select
  user_id as account_id,
  credit_score,
  account_age_days,
  case
    when user_has_2fa_installed = 1 then true
    when user_has_2fa_installed = 0 then false
    else null
  end as has_2fa_installed,
  feature_timestamp
from {{ source('feast', 'user_account_features') }}
