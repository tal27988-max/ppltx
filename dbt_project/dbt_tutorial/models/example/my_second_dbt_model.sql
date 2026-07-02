
-- Use the `ref` function to select from other models
/*
dbt compile --select my_second_dbt_model
*/


select *
from {{ ref('my_first_dbt_model') }}
where id = 1
