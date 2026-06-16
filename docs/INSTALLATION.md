# Installation Guide

## Prerequisites
- Python 3.10+
- Node.js 18+ (optional — only if you want to serve frontend with a dev server)
- MongoDB 6+ (local) OR a MongoDB Atlas connection string
- Flutter 3.0+ (only for the mobile app)
- Git

## 1. Clone the repository
```bash
git clone https://github.com/<your-org>/smart-health-risk-predictor.git
cd smart-health-risk-predictor
```

## 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate           # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then edit secrets
```

### Download datasets
See `backend/datasets/README.md`. Place `heart.csv`, `diabetes.csv`,
`obesity.csv` in `backend/datasets/`.

### Train models
```bash
cd backend
python ml/training.py
```
This produces `saved_models/heart.joblib`, `diabetes.joblib`, `obesity.joblib`
and `metrics.json`.

### Run the API
```bash
python app.py
# → http://localhost:5000
```

## 3. Frontend
```bash
cd frontend
# Option A: open index.html directly
# Option B:
python -m http.server 5500
```
Edit `frontend/js/config.js` so `API_BASE_URL` matches your Flask URL.

## 4. Mobile app
```bash
cd mobile_app_flutter
flutter pub get
# Edit lib/services/api.dart -> baseUrl
flutter run
```

## Common errors

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'flask'` | Activate the venv, re-run `pip install -r requirements.txt` |
| `ServerSelectionTimeoutError` from PyMongo | MongoDB not running or `MONGO_URI` wrong |
| `FileNotFoundError: heart.joblib` | Run `python ml/training.py` first |
| CORS error in browser | Confirm `flask-cors` is installed and the backend is running |
| 401 on protected endpoints | Login first to obtain a JWT, include `Authorization: Bearer <token>` |
