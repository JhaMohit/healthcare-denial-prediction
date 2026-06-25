import psycopg2
import random

conn = psycopg2.connect(
    dbname = "healthcare_denial_prediction",
    user = "jhamohit"
)

cur = conn.cursor()

cur.execute(
    """
    SELECT department_id, department_name
    FROM departments
    """
)

departments = cur.fetchall()

for i in range(7, 201): #As we already have 6 providers in the providers.csv file, we will start from 7 to 200
    provider_name = f"Dr. Provider {i:03d}"
    department = random.choice(departments)
    department_id = department[0]
    specialty = department[1]
    years_of_experience = random.randint(1, 40)
    provider_type = random.choice(
    [
        "Physician",
        "Physician",
        "Physician",
        "Physician",
        "Specialist",
        "Consultant",
        "Nurse Practitioner",
        "Physician Assistant"
    ]
    )

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
conn.commit()
print("Providers inserted successfully!")
cur.close()
conn.close()