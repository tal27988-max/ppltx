-- retentiom

WITH
  install_date AS (
    SELECT
      uid,
      date(min(event_time)) AS install_dt
    FROM `ppltx-ba-course.ds_game.fact`
    GROUP BY ALL
  ),
  activity_date AS (
    SELECT
      uid,
      DATE(event_time) AS dt,
    FROM `ppltx-ba-course.ds_game.fact`
    GROUP BY ALL
  )
SELECT
  install_dt,
  date_diff(dt, install_dt, day) + 1 AS days_in_game,
  COUNT(1) AS total_users
FROM install_date
LEFT JOIN activity_date
  USING (uid)
GROUP BY ALL
ORDER BY 1, 2, 3
