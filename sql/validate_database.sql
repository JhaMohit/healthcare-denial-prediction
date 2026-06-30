-- ============================================================

-- CLAIMS VALIDATION

-- ============================================================

-- Record count
SELECT COUNT(*)
FROM claims;

-- Claim ID range
SELECT
    MIN(claim_id),
    MAX(claim_id)
FROM claims;

-- Status distribution
SELECT
    current_status,
    COUNT(*)
FROM claims
GROUP BY current_status
ORDER BY COUNT(*) DESC;

-- Service date range
SELECT
    MIN(service_date),
    MAX(service_date)
FROM claims;

-- Payer distribution
SELECT
    payer_id,
    COUNT(*)
FROM claims
GROUP BY payer_id
ORDER BY payer_id;

-- ============================================================

-- CLAIM LINES VALIDATION

-- ============================================================

-- Total rows
SELECT COUNT(*)
FROM claim_lines;

-- Average lines per claim
SELECT
    ROUND(AVG(line_count),2)
FROM
(
    SELECT
        claim_id,
        COUNT(*) AS line_count
    FROM claim_lines
    GROUP BY claim_id
) t;

-- Billed amount validation
SELECT
    c.claim_id,
    c.billed_amount,
    SUM(cl.charge_amount) AS calculated_total
FROM claims c
JOIN claim_lines cl
ON c.claim_id = cl.claim_id
GROUP BY
    c.claim_id,
    c.billed_amount
LIMIT 20;

-- Min/Max billed amount
SELECT
    MIN(billed_amount),
    MAX(billed_amount)
FROM claims;

-- ============================================================

-- CLAIM DIAGNOSES VALIDATION

-- ============================================================

-- Total rows
SELECT COUNT(*)
FROM claim_diagnoses;

-- Average diagnoses
SELECT
    ROUND(AVG(diagnosis_count),2)
FROM
(
    SELECT
        claim_id,
        COUNT(*) AS diagnosis_count
    FROM claim_diagnoses
    GROUP BY claim_id
) t;

-- One primary diagnosis
SELECT COUNT(*)
FROM
(
    SELECT
        claim_id
    FROM claim_diagnoses
    WHERE is_primary = TRUE
    GROUP BY claim_id
    HAVING COUNT(*) <> 1
) t; -- should return 0

-- Duplicate diagnosis check 
SELECT
    claim_id,
    diagnosis_id,
    COUNT(*)
FROM claim_diagnoses
GROUP BY
    claim_id,
    diagnosis_id
HAVING COUNT(*) > 1; -- should return no rows

-- ============================================================

-- CLAIM STATUS HISTORY VALIDATION

-- ============================================================

-- Total status events
SELECT COUNT(*)
FROM claim_status_history;

-- Status distribution
SELECT
    status,
    COUNT(*)
FROM claim_status_history
GROUP BY status
ORDER BY COUNT(*) DESC;

-- Sample
SELECT *
FROM claim_status_history
LIMIT 20;

-- ============================================================

-- DENIALS VALIDATION

-- ============================================================

-- Total denials
SELECT COUNT(*)
FROM denials;

-- Line VS Claim denial
SELECT
    CASE
        WHEN claim_line_id IS NULL THEN 'Claim'
        ELSE 'Line'
    END AS denial_scope,
    COUNT(*)
FROM denials
GROUP BY denial_scope;

-- Appeal distribution
SELECT
    appeal_flag,
    COUNT(*)
FROM denials
GROUP BY appeal_flag;

-- Denial rate distribution
SELECT
    denial_reason_id,
    COUNT(*)
FROM denials
GROUP BY denial_reason_id
ORDER BY denial_reason_id;

-- Sample
SELECT *
FROM denials
LIMIT 20;

-- Referential integrity sanity check: Every denial should reference a denied claim
SELECT COUNT(*)
FROM denials d
LEFT JOIN claims c
ON d.claim_id = c.claim_id
WHERE c.claim_id IS NULL; -- Expected o/p - 0