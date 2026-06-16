"""Load saved models and return predictions for incoming JSON payloads."""

import joblib
import numpy as np
from pathlib import Path

# Correct model directory
OUT = Path(__file__).resolve().parents[1] / "ml" / "models"

_cache = {}


def _load(name):

    if name not in _cache:

        filename = f"{name}_model.pkl"

        path = OUT / filename

        if not path.exists():
            raise FileNotFoundError(
                f"Model file not found: {path}"
            )

        _cache[name] = joblib.load(path)

    return _cache[name]


def _predict(name, payload):

    bundle = _load(name)

    features = bundle["features"]
    scaler = bundle["scaler"]
    model = bundle["model"]

    # Check missing fields
    missing = [f for f in features if f not in payload]

    if missing:
        raise ValueError(f"Missing fields: {missing}")

    # Prepare values
    values = []

    for f in features:

        value = payload[f]

        # Convert string categories
        if isinstance(value, str):

            lower = value.lower()

            if lower == "yes":
                value = 1

            elif lower == "no":
                value = 0

            elif lower == "male":
                value = 1

            elif lower == "female":
                value = 0

            elif lower == "sometimes":
                value = 1

            elif lower == "frequently":
                value = 2

            elif lower == "always":
                value = 3

            elif lower == "walking":
                value = 0

            elif lower == "bike":
                value = 1

            elif lower == "motorbike":
                value = 2

            elif lower == "public_transportation":
                value = 3

            elif lower == "automobile":
                value = 4

        values.append(float(value))

    # Create numpy array
    row = np.array([values])

    # Scale
    row = scaler.transform(row)

    # Predict
    pred_raw = model.predict(row)[0]

    # Obesity readable labels
    obesity_labels = {
        0: "Insufficient Weight",
        1: "Normal Weight",
        2: "Overweight Level I",
        3: "Overweight Level II",
        4: "Obesity Type I",
        5: "Obesity Type II",
        6: "Obesity Type III"
    }

    if name == "obesity":
        pred = obesity_labels.get(int(pred_raw), str(pred_raw))
    else:
        pred = int(pred_raw)

    # Probability
    proba = None

    if hasattr(model, "predict_proba"):

        proba_arr = model.predict_proba(row)[0]

        proba = float(max(proba_arr))

    return {
        "disease": name,
        "prediction": pred,
        "probability": round(proba, 4) if proba else None,
        "risk_level": _risk_level(proba, pred, name),
        "recommendations": _recommend(name, pred, proba),
    }


def _risk_level(p, pred=None, name=None):
    if name == "obesity":
        # obesity ke liye pred string hai
        high = ["Obesity Type I", "Obesity Type II", "Obesity Type III"]
        medium = ["Overweight Level I", "Overweight Level II"]
        if pred in high:
            return "high"
        elif pred in medium:
            return "moderate"
        else:
            return "low"
    
    # heart aur diabetes ke liye pred (0 ya 1) use karo
    if pred == 0:
        return "low"
    elif pred == 1:
        if p and p > 0.75:
            return "high"
        else:
            return "moderate"
    return "unknown"


def _recommend(name, pred, proba):

    base = {
        "heart": [
            "Maintain blood pressure below 120/80 mmHg",
            "Exercise 30 minutes a day, 5 days a week",
            "Limit saturated fats and sodium",
        ],

        "diabetes": [
            "Keep fasting glucose below 100 mg/dL",
            "Eat high-fiber, low-glycemic foods",
            "Monitor weight and stay active",
        ],

        "obesity": [
            "Aim for a BMI between 18.5 and 24.9",
            "Track daily calorie intake",
            "Strength + cardio training weekly",
        ],
    }[name]

    if (
        (name != "obesity" and pred == 1)
        or
        (proba and proba > 0.6)
    ):

        base.insert(
            0,
            "Consult a certified physician for a detailed assessment."
        )

    return base


def predict_heart(payload):
    return _predict("heart", payload)


def predict_diabetes(payload):
    return _predict("diabetes", payload)


def predict_obesity(payload):
    return _predict("obesity", payload)