# PathSetu

> **The bridge between disruption and decision.**

A Gemini-powered supply chain intelligence command center for Indian logistics. PathSetu fuses five signal categories — weather, traffic, port congestion, supplier health, and demand — into one **Disruption Probability Score (DPS)**, extends visibility to Tier 2/3 suppliers via phones-as-sensors, and quantifies impact in rupees.

**Built for Google Solution Challenge 2026 · APAC Region**

---

## 🚀 Try the live demo (60 seconds)

1. Open: [https://pathsetu.vercel.app](https://pathsetu.vercel.app)
2. Scroll to **Live Disruption Classification** panel in the Overview tab
3. Pick any Indian news headline from the dropdown
4. Click **"Classify with Gemini →"**
5. Wait 2-3 seconds (first request after idle: ~45 sec — Render free tier wakes from sleep)
6. See real Google Gemini AI classify the disruption with signal type, severity, affected corridors, and recommended action

> **Note for judges:** If the first Gemini call takes 45+ seconds, that's Render's free-tier server waking from sleep. Subsequent calls are fast. We have UptimeRobot pinging the backend every 5 minutes during judging period to minimize cold starts.

---

## 📺 Demo video

[3-minute walkthrough on YouTube](https://youtu.be/your-video-id) *(unlisted)*

---

## 🏗️ Architecture

```
┌──────────────────────────────┐
│  Frontend (Vercel)           │
│  pathsetu.vercel.app         │
│  ├── 6 dashboard tabs        │
│  ├── Live Gemini panel       │
│  └── Risk predictor          │
└──────────────┬───────────────┘
               │ HTTPS
               ▼
┌──────────────────────────────┐
│  Backend API (Render)        │
│  pathsetu-api.onrender.com   │
│  ├── /classify   (POST)      │
│  ├── /sample-feed (GET)      │
│  └── /health     (GET)       │
└──────────────┬───────────────┘
               │ HTTPS
               ▼
┌──────────────────────────────┐
│  Google Gemini 2.5 Flash-Lite │
│  (signal classification)      │
└──────────────────────────────┘
```

---

## 📁 Repository structure

```
pathsetu/
├── frontend/              ← deploys to Vercel
│   └── index.html         ← 4,144 lines: the full dashboard
│
└── backend/               ← deploys to Render
    ├── main.py            ← FastAPI server with Gemini integration
    ├── requirements.txt   ← Python dependencies
    ├── .env.example       ← config template (no real keys)
    ├── .gitignore
    └── README.md          ← backend-specific deployment guide
```

---

## 🛠️ Tech stack

- **Frontend:** HTML, CSS, vanilla JavaScript, Chart.js — deployed on Vercel
- **Backend:** FastAPI · Python 3.11 · httpx · Pydantic — deployed on Render Free Tier
- **AI:** Google Gemini 2.5 Flash-Lite (via Google AI Studio API)
- **Data sources:** Curated Indian supply chain news headlines (15 real-world examples)

### Why these choices

- **FastAPI** — fast async Python framework, auto-generates `/docs` Swagger UI for testing
- **Gemini 2.5 Flash-Lite** — best free-tier rate limits (15 RPM, 1,000 RPD) and fastest responses for classification tasks
- **Render free tier** — sufficient for hackathon submission, single environment variable for API key
- **Vercel** — instant frontend deployment from GitHub, generous free tier

---

## 🚀 Run locally

### Prerequisites
- Python 3.11 or newer
- A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# .\venv\Scripts\activate         # Windows

pip install -r requirements.txt

cp .env.example .env
# Edit .env and paste your Gemini API key

python main.py
# Server runs at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

### Frontend setup

Just open `frontend/index.html` in your browser. The dashboard's `BACKEND_URL` constant points at `http://localhost:8000` for local development. Change it to your deployed Render URL for production.

---

## 🎯 Problem we're solving

Indian supply chains lose thousands of crores annually to disruptions — storms, strikes, port congestion, accidents, supplier failures, and cold-chain breaches — but current systems detect these too late. Signals exist in weather APIs, road telemetry, port feeds, news, and IoT sensors, but they sit in silos. No platform fuses them into a single predictive score that planners can act on in real time.

**The gap is not data. It is fusion, inclusion, coordination, and quantification.**

---

## ✨ Key features (11 differentiators)

1. **Disruption Probability Score (DPS)** — single 0-100 score per shipment
2. **5-Category Signal Fusion** — weather + traffic + port + supplier + demand
3. **Phones-as-Sensors (Tier 2/3)** — supplier smartphones become sensor arrays
4. **Anchor-Buyer Subsidy Model** — three use-case kits (cold chain, fragile, last-mile)
5. **Cross-Team Coordination Layer** — logistics + warehouse + CS + procurement
6. **Internal vs External Response** — separates team actions from customer comms
7. **AI Incident Summaries** — Gemini-generated plain-language explanations
8. **Interactive Risk Predictor** — 3-slider what-if simulator
9. **Live Route Risk Heat Map** — SVG map of Indian corridors
10. **Transparent Risk Breakdown** — signal-type % shown per shipment
11. **Demonstrable Value Trend** — 8-week on-time delivery chart

---

## 🌏 Built for India

- **CSR-fundable** under Companies Act 2013, Schedule VII (ii)+(iii)+(ix)
- **Vertical-agnostic** with three anchor-buyer use cases: cold chain (₹1,200/supplier), fragile goods (₹2,500), last-mile visibility (₹3,500)
- **Aligned with UN SDGs:** 9 (Industry & Innovation), 12 (Responsible Consumption), 3 (Health), 8 (Decent Work), 10 (Reduced Inequalities), 13 (Climate Action)

---

## 👥 Team

**Sushil Singh** — Project Lead · Delhi NCR, India

---

## 📄 License

This project is built for Google Solution Challenge 2026. All code is open source for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- Google Solution Challenge organizers
- Hack2Skill (challenge platform)
- Google Gemini API team
- Indian supply chain professionals whose insights shaped this product
