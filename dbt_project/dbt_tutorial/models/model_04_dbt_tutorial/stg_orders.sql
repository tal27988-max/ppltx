/*

dbt compile --stg_orders
dbt run --stg_orders

*/

{{ config(
    materialized='table',
    schema="dbt_model_04"
) }}

select
    id as order_id,
    user_id as customer_id,
    order_date,
    status

--from `dbt-tutorial`.jaffle_shop.orders
from {{source('jaffle','orders')}}