## Daily ETL

Create schema (dataset)

```
CREATE SCHEMA `my-project-ppltx-sql.daily_etl`
OPTIONS (description = "Contain the Daily ETL process");
```

## steps
- create `increment table` for recent N days (updated data)
- Delete recent 5 days from `Agg table` (Nom Updated data)
- Insert data from `increment table` to `Agg table`
