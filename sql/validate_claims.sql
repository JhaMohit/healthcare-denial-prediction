#REUSABLE DB TABLES SMOKE TEST:
SELECT COUNT(*)
FROM claims;

SELECT
MIN(claim_id),
MAX(claim_id)
FROM claims;

SELECT
current_status,
COUNT(*)
FROM claims
GROUP BY current_status
ORDER BY COUNT(*) DESC;

SELECT
MIN(service_date),
MAX(service_date)
FROM claims;

SELECT
payer_id,
COUNT(*)
FROM claims
GROUP BY payer_id
ORDER BY payer_id;