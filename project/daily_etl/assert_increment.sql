

Assert(
  select Min(t_rows) = 2 t_rows
  from (
        select
            day,
            count(1) as t_rows
        from `my-project-ppltx-sql.daily_etl.daily_inc`
        group by 1
        )

      ) as "Must have 2 rows"