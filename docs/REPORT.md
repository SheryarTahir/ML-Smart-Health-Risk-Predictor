# Project Report — Smart Health Risk Predictor

## 1. Abstract
The Smart Health Risk Predictor is a full-stack application that estimates a
user's risk of three common conditions — heart disease, type-II diabetes,
and obesity — using supervised machine learning on publicly available
clinical datasets. The system exposes its inference via a Flask REST API,
provides a responsive HTML/CSS/JavaScript dashboard, and ships a
cross-platform Flutter mobile client.

## 2. Objectives
- Train and compare three classical ML algorithms (Random Forest, Logistic
  Regression, SVM) on each dataset.
- Persist the best-performing model per disease and serve it through a
  documented REST API.
- Provide a secure, user-authenticated dashboard that visualises risk
  probabilities and historical predictions.
- Demonstrate end-to-end production practices: hashed passwords, JWT auth,
  environment-based config, MongoDB persistence, and cloud deployment.

## 3. System Architecture
```
              ┌──────────────────────┐
              │  Web (HTML/CSS/JS)   │
              │  Flutter mobile app  │
              └──────────┬───────────┘
                         │ HTTPS + JWT
                         ▼
              ┌──────────────────────┐
              │ Flask REST API       │
              │  - auth (JWT)        │
              │  - prediction        │
              │  - history/reports   │
              └────────┬────────┬────┘
                       │        │
              joblib   │        │ pymongo
                       ▼        ▼
              ┌──────────────┐ ┌──────────────┐
              │ Trained ML   │ │ MongoDB      │
              │ artifacts    │ │ users +      │
              │ (.joblib)    │ │ predictions  │
              └──────────────┘ └──────────────┘
```

## 4. Datasets and Preprocessing
| Dataset | Records | Target | Source |
|---------|--------:|--------|--------|
| Heart UCI | 1025 | `target` (0/1) | Kaggle: johnsmith88/heart-disease |
| Pima Diabetes | 768 | `Outcome` (0/1) | Kaggle: uciml/pima-indians-diabetes |
| Obesity | 2111 | `NObeyesdad` (7-class) | Kaggle: fatemehmehrparvar/obesity-levels |

Pipeline (`ml/preprocessing.py`):
1. **Cleaning** — drop duplicate rows, median-impute numeric NaNs,
   mode-impute categorical NaNs.
2. **Encoding** — `LabelEncoder` on all object columns + the target if textual.
3. **Splitting** — stratified 80/20 train/test split with `random_state=42`.
4. **Scaling** — `StandardScaler` fit on train, applied to test.

## 5. Models
| Model | Hyperparameters |
|-------|-----------------|
| Random Forest | `n_estimators=200, random_state=42` |
| Logistic Regression | `max_iter=1000` |
| SVM | `kernel="rbf", probability=True` |

For each dataset, all three are trained, scored on hold-out accuracy and
5-fold cross-validation accuracy, and the highest-accuracy model is saved.
Confusion matrices are captured in `saved_models/metrics.json`.

## 6. API
See `docs/API.md` for full request/response specs. Auth uses
`flask-jwt-extended` with HS256 tokens (24 h expiry).

## 7. Frontend
- Dark healthcare theme, fully responsive (CSS grid + media queries).
- `Chart.js` doughnut & bar visualisations.
- BMI calculator built into the overview tab.
- Forms dynamically generated from `js/predict.js` field definitions so
  schema changes only need one update.

## 8. Mobile App
Flutter app reuses the same REST endpoints, persists the JWT with
`shared_preferences`, and presents Material 3 dark theme screens for
login, registration, dashboard, and per-disease prediction.

## 9. Security
- Passwords hashed with `bcrypt` (default cost factor 12).
- JWT secret loaded from `JWT_SECRET_KEY` env var.
- Server-side validation on every input (`utils/validators.py`).
- CORS configurable per environment.
- MongoDB Atlas IP allow-list in production.

## 10. Deployment
Frontend → Vercel · Backend → Render/Railway · Database → MongoDB Atlas.
Full step-by-step in `docs/DEPLOYMENT.md`.

## 11. Results (sample run)
Numbers depend on dataset version; representative values:
| Disease | Best model | Test accuracy | CV accuracy |
|---------|------------|--------------:|------------:|
| Heart | Random Forest | ~0.98 | ~0.97 |
| Diabetes | Random Forest | ~0.78 | ~0.76 |
| Obesity | Random Forest | ~0.96 | ~0.95 |

## 12. Future Work
- XGBoost / LightGBM benchmarks.
- SHAP-based per-prediction explanations in the dashboard.
- HL7 / FHIR integration for clinical interoperability.
- Background email reports via Celery + Redis.
