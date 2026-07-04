
--insert the incremental data into Agg table

insert into
 `my-project-ppltx-sql.daily_etl.daily_agg`
select *
from `my-project-ppltx-sql.daily_etl.daily_inc`