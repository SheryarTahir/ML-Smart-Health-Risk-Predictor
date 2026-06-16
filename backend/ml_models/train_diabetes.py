"""Train Diabetes classifier (Random Forest)."""
import pandas as pd, joblib, os, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

BASE = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE, "datasets", "diabetes.csv"))

# Zeros in these cols are actually missing values
for c in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    df[c] = df[c].replace(0, np.nan)
    df[c] = df[c].fillna(df[c].median())

X = df.drop("Outcome", axis=1)
y = df["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler().fit(X_train)
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(scaler.transform(X_train), y_train)

pred = model.predict(scaler.transform(X_test))
print(f"Diabetes Model Accuracy: {accuracy_score(y_test, pred):.4f}")
print(classification_report(y_test, pred))

joblib.dump({"model": model, "scaler": scaler, "features": list(X.columns)},
            os.path.join(BASE, "trained", "diabetes_model.pkl"))
print("✅ Saved trained/diabetes_model.pkl")
