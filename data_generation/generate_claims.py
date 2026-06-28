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
        select patient_id
        from patients
        """)
patients = cur.fetchall()

cur.execute(
        """
        select provider_id
        from providers
        """)
providers = cur.fetchall()

cur.execute(
        """
        select payer_id
        from payers
        order by payer_id
        """)
payers = cur.fetchall()
payer_ids = [payer[0] for payer in payers]
payer_weights = [16, 11, 9, 15, 8, 6, 3, 4, 8, 5, 7, 5, 2, 1, 1]

statuses = ["Paid", "Pending", "Denied", "Under Review"]
status_weights = [70, 10, 15, 5]

today = date.today()
two_years_ago = today - timedelta(days = 730)

for i in range(1, 100001):
    claim_number = f"CLM{i:08d}"
    
    patient = random.choice(patients)
    patient_id = patient[0]

    provider = random.choice(providers)
    provider_id = provider[0]

    payer_id = random.choices(
        payer_ids,
        weights = payer_weights,
        k = 1
    )[0]

    random_days = random.randint(0, 730)
    service_date = two_years_ago + timedelta(days = random_days)

    submission_lag = random.randint(1, 15)
    claim_submission_date = service_date + timedelta(days = submission_lag)

    current_status = random.choices(
        statuses,
        weights = status_weights,
        k = 1
    )[0]

    billed_amount = 0
    paid_amount = 0

    cur.execute(
        """
        INSERT INTO claims
        (
            claim_number,
            patient_id,
            provider_id,
            payer_id,
            service_date,
            claim_submission_date,
            current_status,
            billed_amount,
            paid_amount
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            claim_number,
            patient_id,
            provider_id,
            payer_id,
            service_date,
            claim_submission_date,
            current_status,
            billed_amount,
            paid_amount
        )
    )    
    if i % 10000 == 0:
        print(f"{i} claims generated...")

conn.commit()
print("Claims inserted successfully!")

cur.close()
conn.close()