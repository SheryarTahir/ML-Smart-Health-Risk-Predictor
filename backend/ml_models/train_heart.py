"""Train Heart Disease classifier (Random Forest)."""
import pandas as pd, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

BASE = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE, "datasets", "heart.csv"))

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train)
X_test_s  = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train_s, y_train)

pred = model.predict(X_test_s)
print(f"Heart Model Accuracy: {accuracy_score(y_test, pred):.4f}")
print(classification_report(y_test, pred))

joblib.dump({"model": model, "scaler": scaler, "features": list(X.columns)},
            os.path.join(BASE, "trained", "heart_model.pkl"))
print("✅ Saved trained/heart_model.pkl")
