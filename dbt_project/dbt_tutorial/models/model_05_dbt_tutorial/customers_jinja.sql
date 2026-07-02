/*
dbt compile --select model_05_dbt_tutorial
dbt compile --select customers

dbt run --select model_05_dbt_tutorial
dbt run --select customers
*/


{# my jinja comment#}

{{ config(
    materialized='table',
    schema="dbt_model_05",
    persist_docs={"relation": true, "columns": true}
) }}



{% set payment_methods = ["bank_transfer", "credit_card", "gift_card","coupon"] %}

select
    order_id,
    {% for payment_method in payment_methods %}
    sum(case when payment_method = '{{payment_method}}' then amount end) as {{payment_method}}_amount,
    {% endfor %}
    sum(amount) as total_amount
from {{source('data_prep','stripe_payments')}}
group by all


