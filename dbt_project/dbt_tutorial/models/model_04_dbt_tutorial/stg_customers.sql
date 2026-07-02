/*
dbt compile --stg_customers
dbt run --stg_customers

*/

{{ config(
    materialized='table',
    schema="dbt_model_04"
) }}




select
    id as customer_id,
    first_name,
    last_name

--from `dbt-tutorial`.jaffle_shop.customers
from {{source('jaffle','customers')}}