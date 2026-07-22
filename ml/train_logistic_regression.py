"""
03_train_logistic_regression.py
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

if __name__ == "__main__":
    main()