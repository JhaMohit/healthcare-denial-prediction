import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("ml/data/ml_claim_dataset.csv")

# Dataset shape
print(df.shape)

# Column names
print(df.columns)

# Dataset information
df.info()

# First 5 rows
print(df.head())

# Missing Value Summary
missing_summary = pd.DataFrame({
    "Missing Count": df.isnull().sum(),
    "Missing Percentage": (df.isnull().sum() / len(df)) * 100
})

missing_summary = missing_summary[
    missing_summary["Missing Count"] > 0 #Handling only columns with missing values (It won't be useful to see columns with 0 missing values)
]

print("\nMissing Value Summary:")
print(missing_summary)

# Duplicate Rows
duplicate_rows = df.duplicated().sum()

# Duplicate Claim IDs
duplicate_claim_ids = df["claim_id"].duplicated().sum()

print("\nDuplicate Rows:")
print(duplicate_rows)
print("\nDuplicate Claim IDs:")
print(duplicate_claim_ids)

# Target Variable Distribution
print("\nTarget Variable Distribution:")
print(df["target_denied"].value_counts())

print("\nTarget Variable Percentage:")
print(df["target_denied"].value_counts(normalize=True) * 100)

# Visualize Target Variable Distribution
plt.figure(figsize=(6, 4))
df["target_denied"].value_counts().plot(kind="bar")
plt.title("Target Variable Distribution")
plt.xlabel("Target Denied")
plt.ylabel("Number of Claims")
plt.show()

# Statistical Summary
print("\nNumerical Summary")
print(df.describe())

plt.figure(figsize=(8, 5))
sns.histplot(df["billed_amount"], bins = 50, kde=True)
plt.title("Billed Amount Distribution")
plt.xlabel("Billed Amount")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(8, 2))
sns.boxplot(x=df["billed_amount"])
plt.title("Billed Amount Boxplot")
plt.xlabel("Billed Amount")
plt.show()

# Denial Rate by Payer_type
payer_summary = (
    df.groupby("payer_type")
    .agg(
        total_claims = ("claim_id", "count"),
        denied_claims = ("target_denied", "sum"),
    )
)
payer_summary["denial_rate"] = (
    payer_summary["denied_claims"] / payer_summary["total_claims"]
)
print("\nDenial Rate by Payer Type:")
print(payer_summary)

# Denial Rate by Provider_type
provider_summary = (
    df.groupby("provider_type")
    .agg(
        total_claims = ("claim_id", "count"),
        denied_claims = ("target_denied", "sum"),
    )
)
provider_summary["denial_rate"] = (
    provider_summary["denied_claims"] / provider_summary["total_claims"]
)
print("\nDenial Rate by Provider Type:")
print(provider_summary.sort_values("denial_rate", ascending=False))

# Denial Rate by Specialty
specialty_summary = (
    df.groupby("specialty")
    .agg(
        total_claims = ("claim_id", "count"),
        denied_claims = ("target_denied", "sum"),
    )
)
specialty_summary["denial_rate"] = (
    specialty_summary["denied_claims"] / specialty_summary["total_claims"]
)
print("\nDenial Rate by Specialty:")
print(specialty_summary.sort_values("denial_rate", ascending=False))

# Denial Rate by billed_amount_bucket
billed_amount_summary = (
    df.groupby("billed_amount_bucket")
    .agg(
        total_claims = ("claim_id", "count"),
        denied_claims = ("target_denied", "sum"),
    )
)
billed_amount_summary["denial_rate"] = (
    billed_amount_summary["denied_claims"] / billed_amount_summary["total_claims"]
)
print("\nDenial Rate by Billed Amount Bucket:")
print(billed_amount_summary.sort_values("denial_rate", ascending=False))

# Denial Rate by submission_delay_days
submission_delay_summary = (
    df.groupby("submission_delay_days")
    .agg(
        total_claims = ("claim_id", "count"),
        denied_claims = ("target_denied", "sum"),
    )
)
submission_delay_summary["denial_rate"] = (
    submission_delay_summary["denied_claims"] / submission_delay_summary["total_claims"]
)
print("\nDenial Rate by Submission Delay Days:")
print(submission_delay_summary.sort_values("denial_rate", ascending=False))

# ***Relationship Between Features and Target****
# Billed Amount vs Target
print("\nAverage Billed Amount by Claim Status:")

print(
    df.groupby("target_denied")["billed_amount"].describe()
)

# Visualize Billed Amount by Target
plt.figure(figsize=(8,5))
df.boxplot(
    column="billed_amount",
    by="target_denied"
)
plt.title("Billed Amount by Claim Status")
plt.suptitle("")
plt.xlabel("Target Denied")
plt.ylabel("Billed Amount")
plt.show()

#Submission Delay vs Claim Status
print("\nAverage Submission Delay by Claim Status:")

print(
    df.groupby("target_denied")["submission_delay_days"].describe()
)

# Correlation Analysis
numeric_df = df.select_dtypes(include=["int64", "float64"])
correlation_matrix = numeric_df.corr() #We can also keep numeric_df.corr(numeric_only=True) to avoid any future warnings
print(correlation_matrix.round(2))

# Correlation Matrix for Selected Columns (Removing ID Columns)
correlation_columns = [
    "billed_amount",
    "submission_delay_days",
    "target_denied",
    "line_count",
    "average_line_charge",
    "max_line_charge",
    "min_line_charge",
    "diagnosis_count",
    "patient_age",
    "years_of_experience"
]
correlation_matrix = df[correlation_columns].corr()
print(correlation_matrix.round(2))