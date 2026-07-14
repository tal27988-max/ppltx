
--DAU

SELECT
     DATE(event_time) AS dt,
    -- DATE_TRUNC(event_time, MONTH) AS current_month,
    -- DATE_TRUNC(event_time, QUARTER) AS current_quarter,
    -- DATE_TRUNC(event_time, YEAR) AS current_year,
    -- DATE_TRUNC(event_time, WEEK) AS current_week,
    COUNT(DISTINCT uid) AS DAU
FROM
    `ppltx-ba-course.ds_game.fact`
GROUP BY ALL
ORDER BY 1;
