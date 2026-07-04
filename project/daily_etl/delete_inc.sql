--delete from agg table the recent N days


delete from
    `my-project-ppltx-sql.daily_etl.daily_agg`
where
day >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 day)