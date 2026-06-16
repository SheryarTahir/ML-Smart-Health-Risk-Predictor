# REST API Reference

Base URL (local): `http://localhost:5000`

All `/predict/*` and `/history`, `/reports` endpoints require a JWT in
`Authorization: Bearer <token>`.

## POST /register
```json
{ "name": "Jane", "email": "jane@test.com", "password": "secret123" }
```
→ `201` `{ "message": "Registered", "token": "...", "user_id": "..." }`

## POST /login
```json
{ "email": "jane@test.com", "password": "secret123" }
```
→ `200` `{ "token": "...", "user": { "id":"...", "name":"...", "email":"..." } }`

## POST /logout (JWT)
→ `200` `{ "message": "Logged out" }`

## POST /predict/heart (JWT)
Body — 13 fields per UCI heart dataset:
`age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal`

Response:
```json
{
  "disease": "heart", "model": "RandomForest",
  "prediction": 1, "probability": 0.84,
  "risk_level": "high",
  "recommendations": ["Consult a certified physician...", ...]
}
```

## POST /predict/diabetes (JWT)
Body — 8 fields from Pima Indians dataset:
`Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI,
DiabetesPedigreeFunction, Age`

## POST /predict/obesity (JWT)
Body — 16 fields from the obesity dataset:
`Gender, Age, Height, Weight, family_history_with_overweight, FAVC, FCVC,
NCP, CAEC, SMOKE, CH2O, SCC, FAF, TUE, CALC, MTRANS`

## GET /history?limit=50 (JWT)
→ `{ "items": [...], "count": N }`

## GET /reports (JWT)
→ `{ "heart": {"count": 3, "avg_probability": 0.42}, "diabetes": {...}, "obesity": {...} }`

## Error format
```json
{ "error": "Invalid credentials" }
```
HTTP status codes: 400 validation, 401 auth, 404 not found,
409 conflict (email exists), 500 server error.
