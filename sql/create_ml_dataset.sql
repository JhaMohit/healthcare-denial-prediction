/*
=========================================================
ML FEATURE DATASET

One row = One claim

Target:
    target_denied

Purpose:
    Feature engineering dataset for claim denial prediction.

Author:
    Mohit Jha

Version: 1.0
Created: July 2026
Prediction Unit: Claim

=========================================================
*/
DROP TABLE IF EXISTS ml_claim_dataset;
CREATE TABLE ml_claim_dataset AS
WITH
claim_features AS (
    SELECT
        c.claim_id,
        c.patient_id,
        c.provider_id,
        c.payer_id,
        c.service_date,
        c.claim_submission_date,
        c.billed_amount,
        c.claim_submission_date - c.service_date AS submission_delay_days,

        CASE
            WHEN c.current_status = 'Denied' THEN 1
            ELSE 0
        END AS target_denied,

        CASE
            WHEN c.billed_amount <= 200 THEN 'Low'
            WHEN c.billed_amount <= 900 THEN 'Medium'
            WHEN c.billed_amount <= 2400 THEN 'High'
            ELSE 'Very High'
        END AS billed_amount_bucket

    FROM claims c
),

line_features AS (
    SELECT
        cl.claim_id,
        COUNT(*) AS line_count,
        ROUND(AVG(cl.charge_amount), 2) AS average_line_charge,
        MAX(cl.charge_amount) AS max_line_charge,
        MIN(cl.charge_amount) AS min_line_charge
    FROM claim_lines cl
    GROUP BY cl.claim_id
),

diagnosis_features AS (
    SELECT
        cd.claim_id,
        COUNT(*) AS diagnosis_count
    FROM  claim_diagnoses cd
    GROUP BY cd.claim_id
),

primary_diagnosis_features AS (
    SELECT
        cd.claim_id,
        cd.diagnosis_id AS primary_diagnosis_id
    FROM claim_diagnoses cd
    WHERE cd.is_primary IS TRUE
),

payer_features AS (
    SELECT
        c.claim_id,
        p.payer_name,
        p.payer_type 
    FROM claims c 
    LEFT JOIN payers p
    ON
        c.payer_id = p.payer_id
),

patient_features AS (
    SELECT
        c.claim_id,
        pt.age AS patient_age,
        pt.gender AS patient_gender,
        pt.state AS patient_state,
        CASE
            WHEN pt.age < 18 THEN 'Child'
            WHEN pt.age BETWEEN 18 AND 64 THEN 'Adult'
            ELSE 'Senior'
        END AS age_bucket
    FROM claims c
    LEFT JOIN patients pt
    ON c.patient_id = pt.patient_id
),

provider_features AS (
    SELECT
        c.claim_id,
        pr.provider_type,
        pr.specialty,
        pr.department_id,
        pr.years_of_experience,
        CASE
            WHEN pr.years_of_experience <= 5 THEN 'Junior'
            WHEN pr.years_of_experience <= 15 THEN 'Mid'
            WHEN pr.years_of_experience <= 25 THEN 'Senior'
            ELSE 'Expert'
        END AS experience_bucket
    FROM claims c
    LEFT JOIN providers pr
        ON c.provider_id = pr.provider_id
)

SELECT 
    -- Claim Features
    cf.claim_id,
    cf.patient_id,
    cf.provider_id,
    cf.payer_id,
    cf.service_date,
    cf.claim_submission_date,
    cf.billed_amount,
    cf.submission_delay_days,
    cf.target_denied,
    cf.billed_amount_bucket,

    -- Line Features
    lf.line_count,
    lf.average_line_charge,
    lf.max_line_charge,
    lf.min_line_charge,

    -- Diagnosis Features
    df.diagnosis_count,

    -- Primary Diagnosis Features
    pdf.primary_diagnosis_id,

    -- Payer Features
    pf.payer_name,
    pf.payer_type,

    -- Patient Features
    ptf.patient_age,
    ptf.patient_gender,
    ptf.patient_state,
    ptf.age_bucket,

    -- Provider Features
    prf.provider_type,
    prf.specialty,
    prf.department_id,
    prf.years_of_experience,
    prf.experience_bucket

FROM claim_features cf
LEFT JOIN line_features lf 
    ON cf.claim_id = lf.claim_id
LEFT JOIN diagnosis_features df 
    ON cf.claim_id = df.claim_id
LEFT JOIN primary_diagnosis_features pdf 
    ON cf.claim_id = pdf.claim_id
LEFT JOIN payer_features pf 
    ON cf.claim_id = pf.claim_id
LEFT JOIN patient_features ptf 
    ON cf.claim_id = ptf.claim_id
LEFT JOIN provider_features prf 
    ON cf.claim_id = prf.claim_id;