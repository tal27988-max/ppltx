--daily aggregation - Contain the all the aggregated data


-- This query shows a list of the daily top Google Search terms.

create or replace table
    `my-project-ppltx-sql.daily_etl.daily_agg`
 options (description = "Contain aggregated data")
    as
SELECT
   refresh_date AS Day,
   term AS Top_Term,
       -- These search terms are in the top 25 in the US each day.
   rank,
FROM `bigquery-public-data.google_trends.top_terms`
WHERE
   rank < 3
       -- Choose only the top term each day.
   AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 month)
       -- Filter to the last 2 weeks.
GROUP BY Day, Top_Term, rank
ORDER BY Day DESC
   -- Show the days in reverse chronological order.