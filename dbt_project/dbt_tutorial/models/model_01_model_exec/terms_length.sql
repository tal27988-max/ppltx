/*
dbt run --select terms_length
dbt compile --select terms_length
dbt run --select model_01_model_exec
*/

{{ config(
    materialized='table',
    schema="dbt_model_01"
) }}

select *
from {{ref('google_trends')}}