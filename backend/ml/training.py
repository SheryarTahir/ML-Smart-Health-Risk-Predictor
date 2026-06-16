"""Train Random Forest, Logistic Regression, and SVM on each dataset.

Picks the best by accuracy and saves the winning model + scaler + feature list
to backend/saved_models/.

Usage:
    python ml/training.py
"""
import os, json, joblib
from pathlib import Path
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score

from preprocessing import load_csv, encode_categoricals, split_and_scale

ROOT = Path(__file__).resolve().parents[1]
DATASETS = ROOT / "datasets"
OUT = ROOT / "saved_models"
OUT.mkdir(exist_ok=True)

DISEASES = {
    "heart":    {"file": "heart.csv",    "target": "target"},
    "diabetes": {"file": "diabetes.csv", "target": "Outcome"},
    "obesity":  {"file": "obesity.csv",  "target": "NObeyesdad"},
}

MODELS = {
    "RandomForest":       RandomForestClassifier(n_estimators=200, random_state=42),
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "SVM":                SVC(probability=True, kernel="rbf"),
}


def train_one(name, cfg):
    print(f"\n=== {name.upper()} ===")
    df = load_csv(DATASETS / cfg["file"])
    df, encoders = encode_categoricals(df, cfg["target"])
    X_train, X_test, y_train, y_test, scaler, features = split_and_scale(df, cfg["target"])

    results, trained = {}, {}
    for mname, model in MODELS.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        acc = accuracy_score(y_test, pred)
        cv = cross_val_score(model, X_train, y_train, cv=5).mean()
        cm = confusion_matrix(y_test, pred).tolist()
        results[mname] = {"accuracy": float(acc), "cv_accuracy": float(cv), "confusion_matrix": cm}
        trained[mname] = model
        print(f"  {mname:20s} acc={acc:.4f}  cv={cv:.4f}")

    best_name = max(results, key=lambda k: results[k]["accuracy"])
    best_model = trained[best_name]
    print(f"  -> best: {best_name}")

    joblib.dump({
        "model": best_model,
        "scaler": scaler,
        "features": features,
        "encoders": {k: v.classes_.tolist() for k, v in encoders.items()},
        "best_name": best_name,
    }, OUT / f"{name}.joblib")

    return {"best": best_name, "results": results, "features": features}


def main():
    summary = {}
    for name, cfg in DISEASES.items():
        if not (DATASETS / cfg["file"]).exists():
            print(f"!! Missing dataset {cfg['file']} — see datasets/README.md")
            continue
        summary[name] = train_one(name, cfg)
    (OUT / "metrics.json").write_text(json.dumps(summary, indent=2))
    print("\nSaved metrics to saved_models/metrics.json")


if __name__ == "__main__":
    main()
