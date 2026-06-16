"""Shared preprocessing utilities for all three datasets."""
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


def load_csv(path):
    df = pd.read_csv(path)
    # 1. drop exact duplicates
    df = df.drop_duplicates()
    # 2. fill numeric NaNs with median, categorical with mode
    for col in df.columns:
        if df[col].dtype.kind in "biufc":
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode().iloc[0])
    return df


def encode_categoricals(df, target_col):
    encoders = {}
    for col in df.columns:
        if df[col].dtype == "object" and col != target_col:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    if df[target_col].dtype == "object":
        le = LabelEncoder()
        df[target_col] = le.fit_transform(df[target_col].astype(str))
        encoders["__target__"] = le
    return df, encoders


def split_and_scale(df, target_col, test_size=0.2, random_state=42):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test, scaler, list(X.columns)
