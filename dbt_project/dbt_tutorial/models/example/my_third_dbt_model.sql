/*

New model add in the dbt course demonstration

dbt run --select my_third_dbt_model.sql
dbt compile --select my_third_dbt_model.sql
*/


SELECT
id,
generate_uuid() as userId
FROM
UNNEST(GENERATE_ARRAY(1, 10)) AS id