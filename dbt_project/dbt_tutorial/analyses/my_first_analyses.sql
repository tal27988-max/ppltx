/*

dbt compile --select my_first_analyses
dbt run --select my_first_analyses -- לא עובד על אנליסיס

*/

select *
from {{ref('my_first_seeds')}}