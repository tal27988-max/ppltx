/*

Nee model add in the dbt course demonstration

dbt run --select my_forth_dbt_model

dbt compile --select my_forth_dbt_model
*/


select *
from {{ref('my_third_dbt_model')}}
order by length(userId) desc