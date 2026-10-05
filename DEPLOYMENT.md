# MPath Career Counselling - Production Deployment Guide

This guide details the deployment of MPath Career Counselling to production environments (specifically Render Web Services and local staging).

---

## 1. Architecture Overview

- **Framework**: Flask (Application Factory / Modular Blueprints)
- **Production WSGI Server**: Gunicorn (`gunicorn app:app`)
- **Database**: SQLite (local/default) or PostgreSQL (recommended for persistent production on Render)
- **Primary Entry Point**: `app.py` (`app` object)
- **Runtime**: Python 3.11+

---

## 2. Required Environment Variables

Configure the following variables in your Render Dashboard (`Environment` tab) or local `.env`:

| Variable Name | Required | Default / Description |
|---|---|---|
| `FLASK_ENV` | Yes | Set to `production` |
| `FLASK_DEBUG` | Yes | Set to `False` (never run with debug in production) |
| `SECRET_KEY` | Yes | Cryptographically secure random secret string for session signing |
| `PORT` | Auto | Provided automatically by Render (defaults to `5000` locally) |
| `DATABASE_URL` | Optional | PostgreSQL connection URI (`postgresql://user:pass@host:5432/dbname`). If omitted, falls back to local SQLite |
| `GEMINI_API_KEY` | Optional | Google Gemini API key for AI Career Mentor guidance |
| `OPENAI_API_KEY` | Optional | Alternative OpenAI API key for AI Career Mentor |

---

## 3. Local Installation & Development

### Setup Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Initialize Database & Seed Content
```bash
python seed.py
```
This populates:
- 214 authentic career paths
- 1,946 verified colleges
- 95 national & state government examinations
- 70 national scholarships
- 120 AICTE/career internships

### Run Locally
```bash
python app.py
```
Access at `http://127.0.0.1:5000/`.

---

## 4. Production Deployment on Render

### Method A: Automated Deployment via `render.yaml`
1. Connect your GitHub repository (`https://github.com/25f1002767/career-path-India-.git`) to Render.
2. Render detects `render.yaml` automatically.
3. Add any required secret variables (`SECRET_KEY`, `GEMINI_API_KEY`, optional `DATABASE_URL`) in the Render Dashboard.

### Method B: Manual Render Web Service Creation
1. Go to **Render Dashboard** → **New Web Service**.
2. Connect repository `25f1002767/career-path-India-`.
3. Set the following configuration:
   - **Environment**: `Python`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt && python seed.py`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free` or `Starter`
   - **Health Check Path**: `/health`
4. In **Environment Variables**:
   - `FLASK_ENV` = `production`
   - `FLASK_DEBUG` = `False`
   - `SECRET_KEY` = `<secure-random-key>`
   - `PYTHON_VERSION` = `3.11.9`
   - `GEMINI_API_KEY` = `<your-gemini-key>` (if using AI mentor)

---

## 5. Post-Deployment Verification

Verify each item after deployment:

1. **Health Check**:
   ```
   GET https://your-app.onrender.com/health
   Response: 200 OK {"status": "healthy", ...}
   ```
2. **Homepage**: Load `/` and verify career counts and college registries display accurately.
3. **Colleges Module**: Browse `/colleges`, test state/course filters, and view detail pages.
4. **Careers Module**: Browse `/careers`, test search, view roadmaps, and compare careers.
5. **Scholarships**: Check `/scholarships` and ensure external official portal links function properly.
6. **Career Assessment**: Take the assessment flow at `/assessment`.
7. **Authentication**: Test registration, login, and protected student/admin routes.
