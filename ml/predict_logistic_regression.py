"""
predict_logistic_regression.py

Author: Mohit Jha

Project:
    Healthcare Claim Denial Prediction

Purpose:
    Uses the trained Logistic Regression model to
    generate predictions for unseen healthcare claims.

Responsibilities:
    • Load trained Logistic Regression model
    • Predict claim status
    • Return predictions
"""

from train_logistic_regression import train_model
import pandas as pd

def predict_model():
    """
    Generates predictions using the trained
    Logistic Regression model.
    Returns:
        Predicted class labels.
    """
    (
        model,
        _,
        X_test_processed,
        _,
        y_test,
        _
    ) = train_model()

    #Predict class labels for the test set
    predictions = model.predict(
        X_test_processed
    )

    probabilities = model.predict_proba(
    X_test_processed
    )

    return (
        predictions,
        probabilities,
        y_test
    )

def main():
    (
        predictions,
        probabilities,
        y_test
    ) = predict_model()

    print(type(predictions))
    print(predictions.shape)
    print(predictions[:10])  # Print first 10 predictions
    print(type(probabilities))
    print(probabilities.shape)
    print(probabilities[:10])  # Print first 10 probabilities

if __name__ == "__main__":
    main()