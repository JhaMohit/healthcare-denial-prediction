import psycopg2
import random
from datetime import date, timedelta
from decimal import Decimal

conn = psycopg2.connect(
    dbname = "healthcare_denial_prediction",
    user = "jhamohit"
)
cur = conn.cursor()

cur.execute(
    """
    SELECT 
    procedure_id,
    base_price
    FROM procedure_codes
    """
)
procedures = cur.fetchall()

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
    number_of_lines = random.choices(
        [1, 2, 3, 4, 5],
        weights = [35, 30, 20, 10, 5],
        k = 1
    )[0]
    claim_total = Decimal("0.00")
    for line_number in range(1, number_of_lines +1):
        procedure = random.choice(procedures)
        procedure_id = procedure[0]
        base_price = procedure[1]
        variation = Decimal(str(random.uniform(0.90, 1.10)))
        charge_amount = (base_price * variation).quantize(
            Decimal("0.01")
        )
        cur.execute(
            """
            INSERT INTO claim_lines
            (
                claim_id,
                line_number,
                procedure_id,
                charge_amount
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                claim_id,
                line_number,
                procedure_id,
                charge_amount
            )
        )
        claim_total += charge_amount
    cur.execute(
        """
        update claims
        set billed_amount = %s
        where claim_id = %s
        """,
        (claim_total,
            claim_id)
    )
    if claim_id % 10000 == 0:
        print(f"{claim_id} claims processed...")
conn.commit()
cur.close()
conn.close()