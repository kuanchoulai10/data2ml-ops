# dbt Implementation (Hands-on)

## Sources

```yaml title="_sources.yml"
--8<-- "./dbt/models/staging/_sources.yml"
```

## Staging

- naming convention: `stg__<src>__<tbl>`

### stg__feast__transactions

```sql title="stg__feast__transactions.sql"
--8<-- "./dbt/models/staging/stg__feast__transactions.sql"
```

```yaml title="stg__feast__transactions.yml"
--8<-- "./dbt/models/staging/stg__feast__transactions.yml"
```

### stg__feast__acct_fraud_7d

```sql title="stg__feast__acct_fraud_7d.sql"
--8<-- "./dbt/models/staging/stg__feast__acct_fraud_7d.sql"
```

```yaml title="stg__feast__acct_fraud_7d.yml"
--8<-- "./dbt/models/staging/stg__feast__acct_fraud_7d.yml"
```

### stg__feast__acct_profiles

```sql title="stg__feast__acct_profiles.sql"
--8<-- "./dbt/models/staging/stg__feast__acct_profiles.sql"
```

```yaml title="stg__feast__acct_profiles.yml"
--8<-- "./dbt/models/staging/stg__feast__acct_profiles.yml"
```


## Intermediate

### int__feast__acct_num_txns

```sql title="int__feast__acct_num_txns.sql"
--8<-- "./dbt/models/intermediate/int__feast__acct_num_txns.sql"
```

### int__feast__acct_num_txns__extented

```sql title="int__feast__acct_num_txns__extented.sql"
--8<-- "./dbt/models/intermediate/int__feast__acct_num_txns__extented.sql"
```


## Marts

### feat_acct_num_txns_7d

```sql title="feat_acct_num_txns_7d.sql"
--8<-- "./dbt/models/marts/accounts/feat_acct_num_txns_7d.sql"
```

### feat_acct_fraud_7d

```sql title="feat_acct_fraud_7d.sql"
--8<-- "./dbt/models/marts/accounts/feat_acct_fraud_7d.sql"
```

### feat_acct_profiles

```sql title="feat_acct_profiles.sql"
--8<-- "./dbt/models/marts/accounts/feat_acct_profiles.sql"
```

## Exposures

```yaml title="exposures.yml"
--8<-- "./dbt/models/marts/accounts/exposures.yml"
```
