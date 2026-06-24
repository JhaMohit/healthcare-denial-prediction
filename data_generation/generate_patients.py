import psycopg2
import random

conn = psycopg2.connect(
    dbname="healthcare_denial_prediction",
    user="jhamohit"
)

cur = conn.cursor()

states = [
    "CA",
    "TX",
    "FL",
    "NY",
    "IL",
    "PA",
    "OH",
    "GA",
    "NC",
    "MI"
]

for i in range (1, 10001):
    age = random.randint(0, 100)
    gender = random.choice(["Male", "Female"])
    state = random.choice(states)
    member_id = f"MEM{i:06d}"

    cur.execute(
        """
        INSERT INTO patients
        (
            age,
            gender,
            state,
            insurance_member_id
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            age,
            gender,
            state,
            member_id
        )
    )
conn.commit()
print("Patients inserted successfully!")
cur.close()
conn.close()