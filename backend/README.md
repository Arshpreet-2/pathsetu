# PathSetu Backend

> *The bridge between disruption and decision.*

Gemini-powered supply chain disruption classification API for [PathSetu](https://github.com/arshpreeetahuja/pathsetu) — the Google Solution Challenge 2026 submission by Team PathSetu, B.Tech., Second Year,  IGDTUW-Delhi.

This backend takes Indian supply chain news headlines and uses **Google Gemini** to classify them into structured disruption signals (weather, traffic, port, supplier, demand) with severity, affected corridors, and recommended actions.

---

## What it does

```
POST /classify
{
  "headline": "NH-44 closed near Indore due to monsoon flooding"
}

→ Gemini analyses
↓

{
  "signal_type": "weather",
  "severity": "high",
  "affected_corridors": ["NH-44", "Mumbai-Delhi corridor"],
  "suggested_action": "Reroute pharma shipments via NH-7",
  "confidence": 0.92,
  "reasoning": "Monsoon flooding on a major NS corridor; multi-state freight impact."
}
```

---

## Quick start (local development)

### Prerequisites
- Python 3.11 or newer ([download here](https://www.python.org/downloads/))
- Your Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Step 1 — Clone or download this folder

If you got this as a zip, unzip it. If from GitHub:
```
git clone https://github.com/YOUR-USERNAME/pathsetu.git
cd pathsetu/backend
```

### Step 2 — Create your local `.env` file

Copy the template:
- **Mac/Linux:** `cp .env.example .env`
- **Windows:** `copy .env.example .env`

Open `.env` in any text editor (Notepad works) and replace the placeholder with your real Gemini API key:

```
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

⚠️ **Never commit `.env` to GitHub.** It's already in `.gitignore`.

### Step 3 — Install dependencies

```
pip install -r requirements.txt
```

If you get errors, try:
- Mac/Linux: `pip3 install -r requirements.txt`
- Windows: `python -m pip install -r requirements.txt`

### Step 4 — Run the server

```
python main.py
```

You should see:
```
PathSetu API starting up...
Gemini model: gemini-1.5-flash
API key configured: True
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5 — Test it

Open your browser to **http://localhost:8000/docs** — you'll see an interactive Swagger UI.

Try the `/classify` endpoint:
1. Click "POST /classify" → "Try it out"
2. In the request body, replace with:
   ```json
   {"headline": "NH-44 closed near Indore due to monsoon flooding"}
   ```
3. Click "Execute"
4. You should see a real Gemini classification appear ✓

If you see this, **the backend is working with real Gemini calls**.

---

## Deploying to Render.com (free hosting)

### Step 1 — Push code to GitHub

If you don't have a repo yet:
```
cd pathsetu/backend
git init
git add .
git commit -m "Initial backend with Gemini classification"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/pathsetu.git
git push -u origin main
```

### Step 2 — Create Render web service

1. Go to https://dashboard.render.com/
2. Click **New +** → **Web Service**
3. Connect your GitHub account if not done yet
4. Pick the `pathsetu/backend` repo
5. Configure:
   - **Name:** `pathsetu-api`
   - **Region:** Singapore (closest to India)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

### Step 3 — Add API key as environment variable

Before clicking "Create", scroll to **Environment Variables**:

- **Key:** `GEMINI_API_KEY`
- **Value:** `AIzaSy...your-real-key-here`

Click **Add**.

### Step 4 — Deploy

Click **Create Web Service**.

First build takes 3-5 minutes. When done, you'll get a URL like:
```
https://pathsetu-api.onrender.com
```

### Step 5 — Verify deployed API

Visit `https://pathsetu-api.onrender.com/` — should show service status JSON.

Visit `https://pathsetu-api.onrender.com/docs` — interactive API tester.

⚠️ **First request after idle:** Render's free tier sleeps after 15 minutes of inactivity. The first request takes 30-50 seconds to wake up. Subsequent requests are fast. For demo day, hit the URL once before recording to warm it up.

---

## Endpoints reference

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Service status + endpoint list |
| GET | `/health` | Health check |
| POST | `/classify` | Classify a headline via Gemini |
| GET | `/sample-feed` | Pre-configured Indian headlines for demo |
| GET | `/docs` | Interactive Swagger UI |

---

## How the dashboard uses this

In your `index.html`, the "Refresh Alerts" button will call:

```javascript
const response = await fetch('https://pathsetu-api.onrender.com/classify', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    headline: "NH-44 closed near Indore due to monsoon flooding"
  })
});
const data = await response.json();
// data.signal_type, data.severity, data.affected_corridors, etc.
```

Frontend integration code will be added to `index.html` after backend deployment.

---

## Troubleshooting

**`GEMINI_API_KEY not set`**
- Local: check `.env` exists and has the key
- Render: check Environment Variables panel

**`502 Bad Gateway from Gemini`**
- Most likely: invalid API key. Re-create at https://aistudio.google.com/
- Or: model name wrong. Check `GEMINI_MODEL` env var

**`Render service sleeping`**
- Free tier sleeps after 15 min idle. First call is slow. Hit `/health` 30 sec before demo.

**`CORS error in browser console`**
- Backend's CORS is set to `*` (allow all). If still seeing errors, check the URL spelling.

---

## Files in this repo

| File | What it is |
|------|-----------|
| `main.py` | FastAPI server with Gemini classification |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |
| `.gitignore` | Excludes `.env` and other secrets from git |
| `README.md` | This file |

---

## Built with

- **Google Gemini 1.5 Flash** — disruption classification
- **FastAPI** — modern Python web framework
- **httpx** — async HTTP client for Gemini calls
- **Render.com** — free hosting for the live demo

---

**Author:**  Team PathSetu, B.Tech., Second Year,  IGDTUW-Delhi
**For:** Google Solution Challenge 2026, APAC region
