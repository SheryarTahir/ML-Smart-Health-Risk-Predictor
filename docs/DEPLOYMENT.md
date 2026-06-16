# Deployment Guide

## Architecture
```
[ Vercel ]   static  →  [ Render / Railway ]  Flask + ML  →  [ MongoDB Atlas ]
```

## 1. MongoDB Atlas
1. Create a free cluster at https://www.mongodb.com/cloud/atlas
2. Add a database user, allow your IP (or `0.0.0.0/0` for dev)
3. Copy the connection string into `MONGO_URI`

## 2. Backend on Render
1. Push the repo to GitHub.
2. Create a new **Web Service** at https://render.com → connect repo.
3. Root: `backend/`
4. Build command: `pip install -r requirements.txt && python ml/training.py`
5. Start command: `gunicorn app:create_app()`
6. Environment variables:
   - `SECRET_KEY`, `JWT_SECRET_KEY` — long random strings
   - `MONGO_URI` — from Atlas
   - `MONGO_DB` — e.g. `health_predictor`
7. Note the public URL: e.g. `https://shrp-api.onrender.com`

### Backend on Railway (alternative)
- New project → Deploy from GitHub.
- Same env vars; Railway auto-detects the `Procfile`.

## 3. Frontend on Vercel
1. Push the repo to GitHub.
2. https://vercel.com → New Project → root = `frontend/`.
3. Framework preset: **Other**.
4. Edit `frontend/js/config.js`:
   ```js
   window.API_BASE_URL = "https://shrp-api.onrender.com";
   ```
5. Deploy → custom domain optional.

## 4. Mobile app
- Update `mobile_app_flutter/lib/services/api.dart` → `baseUrl` to the
  production API URL.
- Build:
  ```bash
  flutter build apk --release
  flutter build ios --release
  ```

## Environment Variables Checklist
| Variable | Where | Example |
|----------|-------|---------|
| `SECRET_KEY` | backend | `openssl rand -hex 32` |
| `JWT_SECRET_KEY` | backend | `openssl rand -hex 32` |
| `MONGO_URI` | backend | `mongodb+srv://...` |
| `MONGO_DB` | backend | `health_predictor` |
| `PORT` | backend | `10000` (Render injects) |
| `API_BASE_URL` | frontend `config.js` | `https://shrp-api.onrender.com` |

## Production hardening
- Restrict CORS origins to your real frontend URL.
- Use HTTPS only (Render/Vercel provide it).
- Rotate `JWT_SECRET_KEY` periodically.
- Enable MongoDB Atlas IP allowlist.
- Add rate-limiting (e.g. `flask-limiter`) on auth endpoints.
