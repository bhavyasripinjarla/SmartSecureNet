import pandas as pd

def preprocess_data(df):
    df = df.dropna()
    df["Label"] = df["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)
    X = df.drop("Label", axis=1)
    y = df["Label"]
    return X, y
