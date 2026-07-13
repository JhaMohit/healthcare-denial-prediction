"""
data_loader.py
Author: Mohit Jha
Project:
    Healthcare Claim Denial Prediction
Purpose:
    Loads the raw healthcare claims dataset and returns
    it as a pandas DataFrame.
Responsibilities:
    • Load raw dataset
    • Return DataFrame
"""

import pandas as pd

def load_data():
    """
    Loads the raw healthcare claims dataset.
    Returns:
        pandas.DataFrame:
            Raw healthcare claims dataset.
    """
    return pd.read_csv("ml/data/raw/ml_claim_dataset.csv")

def main():
    df = load_data()
    print("Dataset Loaded Successfully!")
    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    main()