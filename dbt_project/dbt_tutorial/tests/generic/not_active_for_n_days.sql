not_active_for_n_days.sql


{% test not_active_for_n_days(model , column_name)  %}

select {{column_name}}
from {{model}}
--where TRIM({{column_name}}) =''
where date_diff(current_date(),{{column_name}},day) > 7

{% endtest %}