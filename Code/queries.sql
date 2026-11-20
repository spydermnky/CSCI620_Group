USE GDELT;

-- QUERY 1: Conflict Internsity by country & month
SELECT ag.ActionGeo_CountryCode AS country, 
  DATE_FORMAT(p.`Day`, '%Y-%m') AS month, COUNT(*) AS n_events,
  ROUND(AVG(ea.GoldsteinScale), 3) AS avg_goldstein, ROUND(AVG(ei.AvgTone), 3) AS avg_tone, 
  SUM(ea.QuadClass = 4) AS material_conflict
FROM ParticipatesIn p
JOIN EventAction ea ON ea.EventCode = p.EventCode
JOIN EventImportance ei ON ei.GlobalEventId = p.GlobalEventId
JOIN ActionGeo ag ON ag.GlobalEventId = p.GlobalEventId
WHERE p.`Day` BETWEEN '2019-11-01' AND '2020-11-30' 
     AND ag.ActionGeo_CountryCode IS NOT NULL
GROUP BY ag.ActionGeo_CountryCode, DATE_FORMAT(p.`Day`, '%Y-%m')
HAVING COUNT(*) >= 50
ORDER BY avg_goldstein ASC, n_events DESC
LIMIT 25;

-- QUERY 2: Most adversarial actor pairs
SELECT a1.ActorCode AS src_code, a1.ActorName AS src_name, 
  a2.ActorCode AS tgt_code, a2.ActorName AS tgt_name, 
  COUNT(*) AS total_events, SUM(ea.QuadClass = 4) AS conflict_events,
  ROUND(SUM(ea.QuadClass = 4) / COUNT(*), 3) AS conflict_share, ROUND(AVG(ea.GoldsteinScale), 2) AS avg_goldstein
FROM ParticipatesIn p
JOIN EventAction ea ON ea.EventCode = p.EventCode
JOIN Actor a1 ON a1.ActorCode = p.Actor1
JOIN Actor a2 ON a2.ActorCode = p.Actor2
WHERE a1.ActorCode <> a2.ActorCode
GROUP BY a1.ActorCode, a1.ActorName, a2.ActorCode, a2.ActorName
HAVING COUNT(*) >= 100
ORDER BY conflict_share DESC, conflict_events DESC
LIMIT 25;

-- QUERY 3: Outlets that cover the conflict most heavily
SELECT src.domain, COUNT(*) AS n_events,
  SUM(src.QuadClass = 4) AS conflict_events, ROUND(SUM(src.QuadClass = 4) / COUNT(*), 3) AS conflict_share,
  ROUND(AVG(src.AvgTone), 3) AS avg_tone, ROUND(AVG(src.NumArticles), 2) AS avg_articles
FROM (
        SELECT  SUBSTRING_INDEX(SUBSTRING_INDEX(
                SUBSTRING_INDEX(dm.SourceURL, '://', -1), '/', 1), '?', 1) AS domain,
                ea.QuadClass AS QuadClass, ei.AvgTone AS AvgTone, ei.NumArticles AS NumArticles
        FROM DataManagement dm
        JOIN ParticipatesIn p ON p.GlobalEventId = dm.GlobalEventId
        JOIN EventAction ea ON ea.EventCode = p.EventCode
        JOIN EventImportance ei ON ei.GlobalEventId = dm.GlobalEventId
        WHERE dm.SourceURL IS NOT NULL
) AS src
GROUP BY src.domain
HAVING COUNT(*) >= 100
ORDER BY conflict_share DESC, n_events DESC
LIMIT 25;

-- QUERY 4: Escalation spike detection
WITH daily AS (
  SELECT ag.ActionGeo_CountryCode AS country, p.`Day` AS d, COUNT(*) AS conflict_events,
  ROUND(AVG(ea.GoldsteinScale), 3) AS avg_goldstein
    FROM ParticipatesIn p
    JOIN EventAction ea ON ea.EventCode = p.EventCode
    JOIN ActionGeo ag ON ag.GlobalEventId = p.GlobalEventId
    WHERE ea.QuadClass = 4 AND ag.ActionGeo_CountryCode IS NOT NULL
    GROUP BY ag.ActionGeo_CountryCode, p.`Day`
),
smoothed AS (
    SELECT country, d, conflict_events, avg_goldstein,
      ROUND(AVG(conflict_events) OVER (PARTITION BY country ORDER BY d ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING), 2) AS trailing_7d,
      LAG(conflict_events) OVER (PARTITION BY country ORDER BY d) AS prev_day
    FROM daily
)
SELECT country, d AS spike_date, conflict_events, prev_day, trailing_7d,
  ROUND(conflict_events / NULLIF(trailing_7d, 0), 2) AS spike_multiple, avg_goldstein
FROM smoothed
WHERE trailing_7d >= 3
  AND conflict_events / trailing_7d >= 1.75
ORDER BY spike_multiple DESC, conflict_events DESC
LIMIT 25;

-- QUERY 5: Events near a point
SET @lat = 50.4333;
SET @lon = 30.5167;
SET @radius_km = 150;

SELECT ag.ActionGeo_FullName as place, p.`Day` as d,
  ea.CAMEOCodeDescription AS action, ea.GoldsteinScale AS goldstein, ei.NumArticles AS articles,
  ROUND(6371 * ACOS(LEAST(1.0, COS(RADIANS(@lat)) * COS(RADIANS(ag.ActionGeo_Lat)) * COS(RADIANS(ag.ActionGeo_Long) - RADIANS(@lon))
    + SIN(RADIANS(@lat)) * SIN(RADIANS(ag.ActionGeo_Lat)))), 1) AS km_away
FROM ActionGeo ag
JOIN ParticipatesIn p ON p.GlobalEventId = ag.GlobalEventId
JOIN EventAction ea ON ea.EventCode = p.EventCode
JOIN EventImportance ei ON ei.GlobalEventId = ag.GlobalEventId
WHERE ea.QuadClass = 4
  AND ag.ActionGeo_Lat BETWEEN @lat - (@radius_km / 111) AND @lat + (@radius_km / 111)
  AND ag.ActionGeo_Long BETWEEN @lon - (@radius_km / (111 * COS(RADIANS(@lat)))) AND @lon + (@radius_km / (111 * COS(RADIANS(@lat))))
HAVING km_away <= @radius_km
ORDER BY km_away ASC
LIMIT 25;