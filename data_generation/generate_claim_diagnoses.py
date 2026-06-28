import psycopg2
import random

conn = psycopg2.connect(
    dbname = "healthcare_denial_prediction",
    user = "jhamohit"
)
cur = conn.cursor()

cur.execute(
    """
    select diagnosis_id
    from diagnosis_codes
    """
)
diagnosis_ids = [row[0] for row in cur.fetchall()]

cur.execute(
    """
    select claim_id
    from claims
    order by claim_id
    """
)
claims = cur.fetchall()

for claim in claims:
    claim_id = claim[0]
# We could use:
# for (claim_id,) in claims:
# to unpack the tuple directly, but this version is more explicit and easier to read.
    number_of_diagnoses = random.choices(
        [1, 2, 3, 4],
        weights = [60, 25, 10, 5],
        k = 1
    )[0]
    selected_diagnoses = random.sample(
        diagnosis_ids,
        number_of_diagnoses
    )
    for index, diagnosis_id in enumerate(selected_diagnoses):
        is_primary = (index == 0)
        cur.execute(
            """
            INSERT INTO claim_diagnoses
            (
                claim_id,
                diagnosis_id,
                is_primary
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                claim_id,
                diagnosis_id,
                is_primary
            )
        )
    if claim_id % 10000 == 0:
        print(f"{claim_id} claims processed...")

conn.commit()
print("Claim diagnoses inserted successfully!")
cur.close()
conn.close()