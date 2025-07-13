
-- Query 1: From the two most commonly appearing regions, which is the latest datasource?
WITH top_regions AS (
    SELECT region, COUNT(*) AS total
    FROM trips
    GROUP BY region
    ORDER BY total DESC
    LIMIT 2
)
SELECT t.region, t.datasource, MAX(t.datetime) AS latest_trip
FROM trips t
JOIN top_regions r ON t.region = r.region
GROUP BY t.region, t.datasource
ORDER BY t.region, latest_trip DESC;

-- Query 2: What regions has the "cheap_mobile" datasource appeared in?
SELECT DISTINCT region
FROM trips
WHERE datasource = 'cheap_mobile';
