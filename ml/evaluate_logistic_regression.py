"""
evaluate_logistic_regression.py

Author: Mohit Jha

Project:
    Healthcare Claim Denial Prediction

Purpose:
    Evaluates the performance of the trained
    Logistic Regression model.

Responsibilities:
    • Generate Confusion Matrix
    • Calculate Accuracy
    • Calculate Precision
    • Calculate Recall
    • Calculate F1 Score
    • Generate Classification Report
"""

from predict_logistic_regression import predict_model
import matplotlib.pyplot as plt
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    roc_curve,
    roc_auc_score
)



def evaluate_model():
    """
    Evaluates the Logistic Regression model.

    Returns:
        Dictionary containing evaluation metrics.
    """

    (
        predictions,
        probabilities,
        y_test
    ) = predict_model()

    # Confusion Matrix
    cm = confusion_matrix(
        y_test,
        predictions
    )

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        predictions
    )

    # Precision
    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    # Recall
    recall = recall_score(
        y_test,
        predictions
    )

    # F1 Score
    f1 = f1_score(
        y_test,
        predictions
    )

    # Classification Report
    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    fpr, tpr, thresholds = roc_curve(
        y_test,
        probabilities[:, 1]
    )

    auc = roc_auc_score(
        y_test,
        probabilities[:, 1]
    )

    return {
        "confusion_matrix": cm,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "classification_report": report,
        "probabilities": probabilities,
        "fpr": fpr,
        "tpr": tpr,
        "thresholds": thresholds,
        "auc": auc
    }


def main():

    results = evaluate_model()

    print("\nConfusion Matrix")
    print(results["confusion_matrix"])

    print("\nAccuracy")
    print(f"{results['accuracy']:.4f}")

    print("\nPrecision")
    print(f"{results['precision']:.4f}")

    print("\nRecall")
    print(f"{results['recall']:.4f}")

    print("\nF1 Score")
    print(f"{results['f1_score']:.4f}")

    print("\nClassification Report")
    print(results["classification_report"])

    print("\nROC AUC Score")
    print(f"{results['auc']:.4f}")

    # Plot ROC Curve

    plt.figure(figsize=(8, 6))

    plt.plot(
        results["fpr"],
        results["tpr"],
        label=f"Logistic Regression (AUC = {results['auc']:.4f})"
    )

    # Random Guessing Line
    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        label="Random Classifier"
    )
    
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()