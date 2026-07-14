

-- revenue



-- Daily Revenue
SELECT
  DATE(event_time) AS dt,
  SUM(price) AS t_revenue
FROM `ppltx-ba-course.ds_game.fact`
WHERE event = "InApp_Purchase"
GROUP BY ALL
order by 1


-- ARPDUA - Avg Revenue per per daily active user
SELECT
  DATE(event_time) AS dt,
  COUNT(DISTINCT uid) AS DAU,
  SUM(CASE WHEN event = "InApp_Purchase" THEN price END) AS t_revenue,
  ROUND(
    SUM(CASE WHEN event = "InApp_Purchase" THEN price END) / COUNT(DISTINCT uid),
    1) AS ARPDUA,
  COUNT(DISTINCT CASE WHEN event = "InApp_Purchase" THEN uid END) AS Paying_users
FROM `ppltx-ba-course.ds_game.fact`
GROUP BY ALL
ORDER BY 1


-- ARPU - Avg Revenue Per User
-- ARPPU - Avg Revenue Per Paying User

SELECT
  COUNT(DISTINCT uid) AS T_Users,
  SUM(CASE WHEN event = "InApp_Purchase" THEN price END) AS t_revenue,
  ROUND(
    SUM(CASE WHEN event = "InApp_Purchase" THEN price END) /
    COUNT(DISTINCT uid),
    1
  ) AS ARPU,

  COUNT(DISTINCT CASE WHEN event = "InApp_Purchase" THEN uid END) AS Paying_Users,
  ROUND(
    SUM(CASE WHEN event = "InApp_Purchase" THEN price END) /
    COUNT(DISTINCT CASE WHEN event = "InApp_Purchase" THEN uid END),
    1  ) AS ARPPU

FROM
  `ppltx-ba-course.ds_game.fact`





  -- Daily Conversion ratio (Paying Users)

SELECT
  DATE(event_time) AS dt,
  COUNT(DISTINCT uid) AS DAU,
  COUNT(DISTINCT CASE WHEN event = "InApp_Purchase" THEN uid END) AS Paying_Users,
round(
  COUNT(DISTINCT CASE WHEN event = "InApp_Purchase" THEN uid END) /
  COUNT(DISTINCT uid) ,3) AS daily_paying_users

FROM
  `ppltx-ba-course.ds_game.fact`

GROUP BY ALL
ORDER BY 1