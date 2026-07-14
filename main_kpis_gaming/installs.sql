
--Daily_ install

WITH
  installs AS (
    SELECT
      uid,
      date(min(event_time)) AS install_dt
    FROM `ppltx-ba-course.ds_game.fact`
    GROUP BY ALL
  )
SELECT
  install_dt,
  COUNT(uid) AS installs
FROM installs
GROUP BY ALL
