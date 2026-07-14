

select *
from ppltx-ba-course.ds_game.fact
where uid = '07d7d53d'
order by event_time desc
limit 1000



--data distribution
SELECT
  COUNT(DISTINCT uid) AS unique_users,
  COUNT(DISTINCT event) AS unique_events,
  min(event_time) AS first_event,
  max(event_time) AS last_event,
FROM `ppltx-ba-course.ds_game.fact`
LIMIT 1000

