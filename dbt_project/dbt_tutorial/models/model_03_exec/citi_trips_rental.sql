/*
dbt compile --select model_03_exec
dbt compile --select citi_trips_rental
dbt run --select model_03_exec
dbt run --select citi_trips_rental
*/

{{ config(
    materialized='table',
    schema="dbt_model_03"
) }}




with trips as
(
select
    start_station_name,
    count(*) as T_trips
from {{source('citi','trips')}}
group by all
order by 2 desc
)

select
    name,
    rental_methods,
    T_trips
from trips as t
left join {{source('citi','stations')}} as s
on t.start_station_name = s.name
order by 3 desc
