import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# load dataset
df = pd.read_csv("ml/data/ml_claim_dataset.csv")

# print("Dataset Loaded Successfully!")
# print(df.shape)

# Convert string columns to datetime
df["service_date"] = pd.to_datetime(df["service_date"])
df["claim_submission_date"] = pd.to_datetime(df["claim_submission_date"])

# print(df.dtypes)

# Extract service/submission month and day of week from the datetime columns
df["service_month"] = df["service_date"].dt.month
df["submission_month"] = df["claim_submission_date"].dt.month
df["service_day_of_week"] = df["service_date"].dt.dayofweek #.dt.weekday can also be used -- exactly the same as dayofweek
df["submission_day_of_week"] = df["claim_submission_date"].dt.dayofweek

# print(df[["service_date", 
# "claim_submission_date", 
# "service_month", 
# "submission_month", 
# "service_day_of_week", 
# "submission_day_of_week"]].head())

# Columns to remove before model training
columns_to_drop = [
    "claim_id",
    "patient_id",
    "provider_id",
    "payer_id",
    "primary_diagnosis_id",
    "department_id",
    "service_date",
    "claim_submission_date",
    "age_bucket",
    "experience_bucket"
]
df = df.drop(columns=columns_to_drop)
# print(df.columns)
# print(df.shape)

# Define feature types
ordinal_features = [
    "billed_amount_bucket",
    "patient_gender",
    "payer_type"
]

nominal_features = [
    "payer_name",
    "patient_state",
    "provider_type",
    "specialty"
]

numeric_features = [
    "billed_amount",
    "submission_delay_days",
    "line_count",
    "average_line_charge",
    "max_line_charge",
    "min_line_charge",
    "diagnosis_count",
    "patient_age",
    "years_of_experience",
    "service_month",
    "submission_month",
    "service_day_of_week",
    "submission_day_of_week"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "ordinal",
            OrdinalEncoder(
                categories=[
                    ["Low", "Medium", "High", "Very High"],
                    ["Female", "Male"],
                    ["Commercial", "Government"]
                ]
            ),
            ordinal_features
        ),

        (
            "nominal",
            OneHotEncoder(
                drop="first",
                handle_unknown="ignore"
            ),
            nominal_features
        ),

        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)

X = df.drop(columns=["target_denied"])
y = df["target_denied"]

# print(X.shape)
# print(y.shape)

# print(X.columns)
# print(y.head())

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size = 0.2,
    random_state = 42,
    stratify = y
)
# print("X_train Shape:", X_train.shape)
# print("X_test Shape:", X_test.shape)

# print("y_train Shape:", y_train.shape)
# print("y_test Shape:", y_test.shape)

# Apply preprocessing pipeline
X_train_processed = preprocessor.fit_transform(X_train)
X_test_processed = preprocessor.transform(X_test)

# print(type(X_train_processed))

# print(X_train_processed.shape)
# print(X_test_processed.shape)

# Get feature names after preprocessing
feature_names = preprocessor.get_feature_names_out()
X_train_processed = pd.DataFrame(
    X_train_processed,
    columns=feature_names
)

X_test_processed = pd.DataFrame(
    X_test_processed,
    columns=feature_names
)

print(X_train_processed.head())
print(X_train_processed.columns)