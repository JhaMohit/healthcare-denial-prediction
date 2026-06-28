import psycopg2
import random
from datetime import date, timedelta

conn = psycopg2.connect(
    dbname = "healthcare_denial_prediction",
    user = "jhamohit"
)
cur = conn.cursor()

cur.execute(
    """
    SELECT
        claim_id,
        claim_submission_date,
        current_status
    FROM claims
    ORDER BY claim_id
    """
)
claims = cur.fetchall()

for claim_id, submission_date, current_status in claims:
    cur.execute(
    """
    INSERT INTO claim_status_history
    (
        claim_id,
        status,
        status_date
    )
    VALUES (%s, %s, %s)
    """,
    (
        claim_id,
        "Submitted",
        submission_date
    )
    )
    review_date = submission_date + timedelta(days = random.randint(1, 5))
    if current_status == "Pending":
        cur.execute(
            """
            INSERT INTO claim_status_history
            (
                claim_id,
                status,
                status_date
            )
            VALUES (%s, %s, %s)
            """,
            (
                claim_id,
                "Pending",
                review_date
            )
        )
    else:
        cur.execute(
            """
            INSERT INTO claim_status_history
            (
                claim_id,
                status,
                status_date
            )
            VALUES (%s, %s, %s)
            """,
            (
                claim_id,
                "Under Review",
                review_date
            )
        )
    final_status_date = review_date + timedelta(days = random.randint(3, 15))
    if current_status == "Paid":
        cur.execute(
            """
            INSERT INTO claim_status_history
            (
                claim_id,
                status,
                status_date
            )
            VALUES (%s, %s, %s)
            """,
            (
                claim_id,
                "Paid",
                final_status_date
            )
        )
    elif current_status == "Denied":
        cur.execute(
            """
            INSERT INTO claim_status_history
            (
                claim_id,
                status,
                status_date
            )
            VALUES (%s, %s, %s)
            """,
            (
                claim_id,
                "Denied",
                final_status_date
            )
        )
    if claim_id % 10000 == 0:
        print(f"{claim_id} claims processed...")
conn.commit()
print("Claim status history inserted successfully!")
cur.close()
conn.close()