CREATE TABLE claims (
    claim_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    claim_number VARCHAR(50) NOT NULL UNIQUE,

    patient_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    payer_id INTEGER NOT NULL,

    service_date DATE NOT NULL,
    claim_submission_date DATE NOT NULL,

    billed_amount NUMERIC(12,2) NOT NULL CHECK (billed_amount >= 0),
    paid_amount NUMERIC(12,2) DEFAULT 0 CHECK (paid_amount >= 0),

    current_status VARCHAR(50) NOT NULL,

    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (provider_id) REFERENCES providers(provider_id),
    FOREIGN KEY (payer_id) REFERENCES payers(payer_id)
);
CREATE TABLE claim_lines (
    claim_line_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    claim_id INTEGER NOT NULL,
    procedure_id INTEGER NOT NULL,

    line_number INTEGER NOT NULL,

    charge_amount NUMERIC(12,2) NOT NULL CHECK (charge_amount >= 0),

    CONSTRAINT uq_claim_line_number
        UNIQUE (claim_id, line_number),

    FOREIGN KEY (claim_id)
        REFERENCES claims(claim_id),

    FOREIGN KEY (procedure_id)
        REFERENCES procedure_codes(procedure_id)
);
CREATE TABLE claim_diagnoses (
    claim_diagnosis_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    claim_id INTEGER NOT NULL,
    diagnosis_id INTEGER NOT NULL,

    CONSTRAINT uq_claim_diagnosis
        UNIQUE (claim_id, diagnosis_id),

    FOREIGN KEY (claim_id)
        REFERENCES claims(claim_id),

    FOREIGN KEY (diagnosis_id)
        REFERENCES diagnosis_codes(diagnosis_id)
);
CREATE TABLE claim_status_history (
    status_history_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    claim_id INTEGER NOT NULL,

    status VARCHAR(50) NOT NULL,

    status_date TIMESTAMP NOT NULL,

    CONSTRAINT uq_claim_status_event
        UNIQUE (claim_id, status, status_date),

    FOREIGN KEY (claim_id)
        REFERENCES claims(claim_id)
);
CREATE TABLE denials (

    denial_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    claim_id INTEGER NOT NULL,
    claim_line_id INTEGER,

    denial_reason_id INTEGER NOT NULL,

    denial_date DATE NOT NULL,

    denied_amount NUMERIC(12,2) NOT NULL
        CHECK (denied_amount >= 0),

    appeal_flag BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (claim_id)
        REFERENCES claims(claim_id),

    FOREIGN KEY (claim_line_id)
        REFERENCES claim_lines(claim_line_id),

    FOREIGN KEY (denial_reason_id)
        REFERENCES denial_reason_codes(denial_reason_id)

);