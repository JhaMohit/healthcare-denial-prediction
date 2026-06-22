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