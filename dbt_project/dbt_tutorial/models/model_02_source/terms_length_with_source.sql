/*
dbt run --select terms_length
dbt compile --select terms_length
dbt compile --select model_02_source
dbt run --select model_02_source
dbt run --select model_01_model_exec
*/

{{ config(
    materialized='table',
    schema="dbt_model_02"
) }}

select *
from {{ref('google_trends_with_source')}}
order by length(top_term)desc