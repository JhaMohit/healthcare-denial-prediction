CREATE TABLE departments (
    department_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE providers (
    provider_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    provider_name VARCHAR(100) NOT NULL,
    provider_type VARCHAR(50) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    years_of_experience INTEGER NOT NULL
        CHECK (years_of_experience >= 0),
    department_id INTEGER NOT NULL,

    CONSTRAINT fk_providers_department
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
);
CREATE TABLE payers (
    payer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payer_name VARCHAR(100) NOT NULL UNIQUE,
    payer_type VARCHAR(50) NOT NULL
);