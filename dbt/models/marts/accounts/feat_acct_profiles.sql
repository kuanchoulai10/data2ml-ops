select
  account_id as entity_id,
  credit_score,
  account_age_days,
  has_2fa_installed,
  feature_timestamp
from {{ ref('fraud', 'stg__feast__acct_profiles') }}
