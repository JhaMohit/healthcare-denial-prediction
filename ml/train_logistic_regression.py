"""
train_logistic_regression.py
Author: Mohit Jha
Project:
    Healthcare Claim Denial Prediction
Purpose:
    Trains a Logistic Regression model using the
    preprocessed training dataset.
Responsibilities:
    • Load preprocessed training data
    • Train Logistic Regression model
    • Return trained model
"""

from sklearn.linear_model import LogisticRegression
from preprocessing import preprocess_data
import pandas as pd

def train_model():
    """
    Trains the Logistic Regression model.
    Returns:
        Trained LogisticRegression model.
    """
    (
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor
    ) = preprocess_data()

    # Create Logistic Regression model
    model = LogisticRegression(
        random_state=42
    )

    # Train the model
    model.fit(
        X_train_processed,
        y_train
    )

    return (
        model,
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor
    )

def main():
    (
        model,
        X_train_processed,
        X_test_processed,
        y_train,
        y_test,
        preprocessor
    ) = train_model()

    print(type(model))
    print(model)
    print(model.n_features_in_)
    print(model.intercept_)
    print(model.coef_)
    print(model.n_iter_)

    # Model Interpretation
    feature_names = preprocessor.get_feature_names_out()
    
    print(feature_names)
    print(len(feature_names))
    print(model.coef_.shape)
    print(len(model.coef_[0]))

    coefficient_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Coefficient": model.coef_[0]
        }
    )
    print(coefficient_df)

    #feature with highest positive coefficient
    coefficient_df_positive = coefficient_df.sort_values(
        by="Coefficient", 
        ascending=False
    )
    print("\nTop Positive Coefficients")
    print(coefficient_df_positive.head(10))

    #feature with highest negative coefficient
    coefficient_df_negative = coefficient_df.sort_values(
        by="Coefficient", 
        ascending=True
    )
    print("\nTop Negative Coefficients")
    print(coefficient_df_negative.head(10))

    # Magnitude of coefficients
    coefficient_df["Absolute Coefficient"] = (
        coefficient_df["Coefficient"].abs()
    )

    coefficient_df_absolute = coefficient_df.sort_values(
        by="Absolute Coefficient",
        ascending=False
    )
    print("\nTop Absolute Coefficients")
    print(coefficient_df_absolute.head(10).round(3))

if __name__ == "__main__":
    main()