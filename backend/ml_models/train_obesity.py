"""Train Obesity multi-class classifier (Random Forest)."""
import pandas as pd, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

BASE = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE, "datasets", "obesity.csv"))

# Encode every categorical column
encoders = {}
for col in df.select_dtypes(include="object").columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop("NObeyesdad", axis=1)
y = df["NObeyesdad"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler().fit(X_train)
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(scaler.transform(X_train), y_train)

pred = model.predict(scaler.transform(X_test))
print(f"Obesity Model Accuracy: {accuracy_score(y_test, pred):.4f}")
print(classification_report(y_test, pred))

joblib.dump({
    "model": model, "scaler": scaler,
    "encoders": encoders, "features": list(X.columns),
    "target_classes": list(encoders["NObeyesdad"].classes_),
}, os.path.join(BASE, "trained", "obesity_model.pkl"))
print("✅ Saved trained/obesity_model.pkl")
