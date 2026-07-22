"""
preprocessing.py
Author: Mohit Jha
Purpose:
    Performs feature engineering, train-test splitting,
    categorical encoding, and preprocessing to prepare
    data for machine learning models.
Responsibilities:
    • Feature Engineering
    • Train/Test Split
    • Encode Categorical Features
    • Apply Preprocessing Pipeline
    • Return processed datasets
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from data_loader import load_data
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def preprocess_data():
    """
    Loads the raw claims dataset, performs feature engineering,
    encodes categorical variables, splits the data into train/test
    sets, and applies the preprocessing pipeline.
    Returns:
        X_train_processed
        X_test_processed
        y_train
        y_test
        preprocessor
    """
    # load dataset
    df = load_data()

    # Convert string columns to datetime
    df["service_date"] = pd.to_datetime(df["service_date"])
    df["claim_submission_date"] = pd.to_datetime(df["claim_submission_date"])

    # Extract service/submission month and day of week from the datetime columns
    df["service_month"] = df["service_date"].dt.month
    df["submission_month"] = df["claim_submission_date"].dt.month
    df["service_day_of_week"] = df["service_date"].dt.dayofweek #.dt.weekday can also be used -- exactly the same as dayofweek
    df["submission_day_of_week"] = df["claim_submission_date"].dt.dayofweek

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

    numeric_pipeline = Pipeline(
    steps=[
        (
            "scaler",
            StandardScaler()
        )
    ]
)

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
                numeric_pipeline,
                numeric_features
            )
        ]
    )

    X = df.drop(columns=["target_denied"])
    y = df["target_denied"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size = 0.2,
        random_state = 42,
        stratify = y
    )

    # Apply preprocessing pipeline
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

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

    return (
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor
    )

def main():
    (
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor
    ) = preprocess_data()

    print(f"Training Shape : {X_train_processed.shape}")
    print(f"Testing Shape  : {X_test_processed.shape}")

if __name__ == "__main__":
    main()