import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="healthcare_denial_prediction",
    user="jhamohit"
)

cur = conn.cursor()

# Read departments from CSV
departments = []

file = open("master_data/departments.csv", "r")

next(file) #Skip the header line

for line in file:
    departments.append(line.strip())

file.close()

# Insert departments into database
for department in departments:
    cur.execute(
        """
        INSERT INTO departments (department_name)
        VALUES (%s)
        ON CONFLICT (department_name) DO NOTHING
        """,
        (department,)
    )

conn.commit()

print("Departments inserted successfully!")

file = open("master_data/providers.csv", "r")

next(file)

for line in file:

    values = line.strip().split(",")
    
    provider_name = values[0]
    provider_type = values[1]
    specialty = values[2]
    years_of_experience = int(values[3])
    department_id = int(values[4])

    cur.execute(
        """
        INSERT INTO providers
        (
            provider_name,
            provider_type,
            specialty,
            years_of_experience,
            department_id
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            provider_name,
            provider_type,
            specialty,
            years_of_experience,
            department_id
        )
    )
file.close()
conn.commit()
print("Providers inserted successfully!")


file = open("master_data/payers.csv", "r")

next(file)

for line in file:

    values = line.strip().split(",")
    
    payer_name = values[0]
    payer_type = values[1]

    cur.execute(
        """
        INSERT INTO payers
        (
            payer_name,
            payer_type
        )
        VALUES (%s, %s)
        ON CONFLICT (payer_name) DO NOTHING
        """,
        (
            payer_name,
            payer_type
        )
    )
file.close()
conn.commit()
print("Payers inserted successfully!")


file = open("master_data/diagnosis_codes.csv", "r")

next(file)

for line in file:

    values = line.strip().split(",")
    
    diagnosis_code = values[0]
    diagnosis_description = values[1]

    cur.execute(
        """
        INSERT INTO diagnosis_codes
        (
            diagnosis_code,
            diagnosis_description
        )
        VALUES (%s, %s)
        ON CONFLICT (diagnosis_code) DO NOTHING
        """,
        (
            diagnosis_code,
            diagnosis_description
        )
    )
file.close()
conn.commit()
print("Diagnosis codes inserted successfully!")


file = open("master_data/procedure_codes.csv", "r")

next(file)

for line in file:

    values = line.strip().split(",")
    
    procedure_code = values[0]
    procedure_description = values[1]

    cur.execute(
        """
        INSERT INTO procedure_codes
        (
            procedure_code,
            procedure_description
        )
        VALUES (%s, %s)
        ON CONFLICT (procedure_code) DO NOTHING
        """,
        (
            procedure_code,
            procedure_description
        )
    )
file.close()
conn.commit()
print("Procedure codes inserted successfully!")


file = open("master_data/denial_reason_codes.csv", "r")

next(file)

for line in file:

    values = line.strip().split(",")
    
    denial_reason_code = values[0]
    denial_reason_description = values[1]

    cur.execute(
        """
        INSERT INTO denial_reason_codes
        (
            denial_reason_code,
            denial_reason_description
        )
        VALUES (%s, %s)
        ON CONFLICT (denial_reason_code) DO NOTHING
        """,
        (
            denial_reason_code,
            denial_reason_description
        )
    )
file.close()
conn.commit()
print("Denial reason codes inserted successfully!")
cur.close()
conn.close()