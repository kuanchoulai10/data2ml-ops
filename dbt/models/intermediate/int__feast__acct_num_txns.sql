{{ config(
    materialized='incremental',
    incremental_strategy='microbatch',
    event_time='transaction_date',
    begin='2025-04-20',
    batch_size='day',
    partition_by={
      "field": "transaction_date",
      "data_type": "date",
      "granularity": "day"
    },
    on_schema_change='append_new_columns'
) }}

with transactions as (

    -- this ref will be auto-filtered
    select
      {{ dbt_utils.star(
        ref('fraud', 'stg__feast__transactions')
      ) }}
    from {{ ref('fraud', 'stg__feast__transactions') }}

)

select
  src_account_id as account_id,
  date(created_at) as transaction_date,
  count(*) as num_transactions,
  sum(amount) as total_amount,
  sum(case when amount > 0 then amount else 0 end) as total_deposits,
from transactions
group by account_id, date(created_at)
