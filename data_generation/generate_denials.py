import psycopg2
import random

conn = psycopg2.connect(
    dbname = "healthcare_denial_prediction",
    user = "jhamohit"
)

cur = conn.cursor()

cur.execute(
    """
    SELECT
    claim_id,
    status_date
    FROM claim_status_history
    WHERE status = 'Denied'
    ORDER BY claim_id
    """
)

denied_claims = cur.fetchall()

cur.execute(
    """
    SELECT
        denial_reason_id
    FROM denial_reason_codes
    ORDER BY denial_reason_id
    """
)

denial_reason_ids = [row[0] for row in cur.fetchall()]

denial_reason_weights = [
    18,   # Missing information
    6,    # Duplicate
    6,    # COB
    8,    # Timely filing
    12,   # Fee schedule
    16,   # Medical necessity
    10,   # Non covered
    7,    # Bundled
    5,    # Wrong payer
    2,    # Benefit max
    3,    # Payer policy
    2,    # Deductible
    1,    # Coinsurance
    1,    # Copay
    1     # Benefit plan
]

for claim_id, denial_date in denied_claims:
    cur.execute(
        """
        SELECT
            claim_line_id,
            charge_amount
        FROM claim_lines
        WHERE claim_id = %s
        """,
        (claim_id,)
    )
    
    claim_lines = cur.fetchall()

    denial_scope = random.choices(
        ["Line", "Claim"],
        weights=[70, 30],
        k=1
    )[0]
    
    if denial_scope == "Line":
        selected_line = random.choice(claim_lines)
        claim_line_id = selected_line[0]
        denied_amount = selected_line[1]
    
    else:
        claim_line_id = None
        denied_amount = sum(
            line[1]
            for line in claim_lines
        )

    denial_reason_id = random.choices(
        denial_reason_ids,
        weights=denial_reason_weights,
        k=1
    )[0]

    appeal_flag = random.choices(
        [True, False],
        weights=[25, 75],
        k=1
    )[0]

    cur.execute(
        """
        INSERT INTO denials
        (
            claim_id,
            claim_line_id,
            denial_reason_id,
            denial_date,
            denied_amount,
            appeal_flag
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """,
        (
            claim_id,
            claim_line_id,
            denial_reason_id,
            denial_date,
            denied_amount,
            appeal_flag
        )
    )
    
    if claim_id % 10000 == 0:
        print(f"{claim_id} denied claims processed...")

conn.commit()
print("Denials inserted successfully!")

cur.close()
conn.close()