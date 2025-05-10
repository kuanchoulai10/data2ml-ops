select
  *,
  sum(num_transactions) over (
    partition by account_id
    order by unix_date(transaction_date)
    range between 6 preceding
    and current row
  ) as num_transactions_7d
from {{ ref('fraud', 'int__feast__acct_num_txns') }}
