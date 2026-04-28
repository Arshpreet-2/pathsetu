"""
PathSetu Backend — Gemini-Powered Disruption Classification API
Built for Google Solution Challenge 2026.

Endpoints:
  GET  /              — health check
  GET  /health        — health check (alias)
  POST /classify      — classify a single news headline using Gemini
  GET  /sample-feed   — pre-configured Indian supply chain news for demo

Author:  Team PathSetu, B.Tech., First Year,  IGDTUW-Delhi
"""

import os
import json
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
from dotenv import load_dotenv


# ---- Setup ----

load_dotenv()  # Load .env file if running locally

logging.basicConfig(level=logging.INFO, format='%(asctime)s — %(levelname)s — %(message)s')
log = logging.getLogger("pathsetu")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

if not GEMINI_API_KEY:
    log.warning("GEMINI_API_KEY not set. /classify endpoint will return errors until configured.")


# ---- Lifespan ----

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("PathSetu API starting up...")
    log.info(f"Gemini model: {GEMINI_MODEL}")
    log.info(f"API key configured: {bool(GEMINI_API_KEY)}")
    yield
    log.info("PathSetu API shutting down.")


# ---- App ----

app = FastAPI(
    title="PathSetu Disruption API",
    description="The bridge between disruption and decision. Gemini-powered supply chain disruption classification for Indian logistics.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allows the dashboard (any origin in MVP) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your Vercel domain
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ---- Schemas ----

class ClassifyRequest(BaseModel):
    headline: str = Field(..., min_length=10, max_length=500,
                          description="The news headline to classify.")
    region: Optional[str] = Field(default="India",
                                  description="Geographic region context.")


class ClassifyResponse(BaseModel):
    headline: str
    signal_type: str  # weather | traffic | port | supplier | demand | other
    severity: str     # low | medium | high | critical
    affected_corridors: list[str]
    suggested_action: str
    confidence: float
    reasoning: str
    powered_by: str = "Google Gemini"


# ---- Sample feed (real Indian headlines for reliable demos) ----

SAMPLE_HEADLINES = [
    "NH-44 closed near Indore due to heavy monsoon flooding, trucks rerouted via NH-7",
    "Mumbai port congestion: vessel turnaround time hits 6 days, exporters worried",
    "Truckers' strike in Maharashtra enters third day, supply lines disrupted",
    "Bengaluru-Chennai expressway: multiple accidents, traffic at standstill for 4 hours",
    "Pharma manufacturer Cipla flags raw material shortage from China",
    "Cyclone Remal hits West Bengal, Kolkata port operations suspended",
    "Delhi NCR air quality crashes to 'severe', diesel truck entry restricted",
    "Tamil Nadu rains: rail freight delays of 8-12 hours reported on Chennai routes",
    "Nashik onion farmers' agitation blocks NH-3, vegetable supplies hit Mumbai",
    "Maersk reports container shortage at Mundra port, 3-week wait times",
    "Karnataka transport union announces 24-hour bandh against fuel hike",
    "Heatwave warning: ice-cream and dairy supply chains stressed across North India",
    "Punjab farmer protests block Delhi-Amritsar highway for 18 hours",
    "Gujarat coast: cyclone alert issued for Kandla and Mundra ports",
    "Indian Railways: goods train derailment near Jhansi disrupts 12 routes",
]


# ---- Gemini integration ----

def build_classification_prompt(headline: str, region: str) -> str:
    """Construct the structured prompt for Gemini."""
    return f"""You are a supply chain disruption analyst for Indian logistics. Analyze this news headline and respond ONLY with a valid JSON object — no markdown, no explanation, no code fences.

Headline: "{headline}"
Region: {region}

Required JSON schema:
{{
  "signal_type": "weather" | "traffic" | "port" | "supplier" | "demand" | "other",
  "severity": "low" | "medium" | "high" | "critical",
  "affected_corridors": ["list", "of", "specific", "highways", "or", "regions"],
  "suggested_action": "concise 1-sentence operational recommendation for logistics teams",
  "confidence": 0.0 to 1.0,
  "reasoning": "1-2 sentence explanation of how you classified this"
}}

Rules:
- signal_type is the PRIMARY disruption category
- severity reflects business impact: low (minor delay), medium (regional), high (multi-state), critical (national)
- affected_corridors should mention specific highway numbers (NH-44, etc.), city pairs, or regions
- Output PURE JSON only. No backticks. No "json" prefix. No commentary.

Respond now with the JSON object:"""


async def call_gemini(headline: str, region: str = "India") -> dict:
    """Call Gemini API to classify a headline. Returns parsed JSON."""
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="GEMINI_API_KEY environment variable not configured on the server."
        )

    prompt = build_classification_prompt(headline, region)

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 400,
            "responseMimeType": "application/json"
        }
    }

    headers = {"Content-Type": "application/json"}
    url_with_key = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            response = await client.post(url_with_key, json=payload, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            log.error(f"Gemini API error: {e.response.status_code} {e.response.text}")
            raise HTTPException(
                status_code=502,
                detail=f"Gemini API returned {e.response.status_code}. Check API key and model name."
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Gemini API request timed out.")
        except Exception as e:
            log.error(f"Unexpected Gemini error: {e}")
            raise HTTPException(status_code=500, detail=f"Gemini call failed: {str(e)}")

    try:
        data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        # Clean and parse JSON
        text = text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        parsed = json.loads(text)
        return parsed
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        log.error(f"Failed to parse Gemini response: {e}. Raw: {response.text[:500]}")
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an unparseable response. Try again."
        )


# ---- Endpoints ----

@app.get("/")
async def root():
    """Health check + service info."""
    return {
        "service": "PathSetu Disruption API",
        "tagline": "The bridge between disruption and decision",
        "status": "running",
        "gemini_configured": bool(GEMINI_API_KEY),
        "model": GEMINI_MODEL,
        "endpoints": ["/", "/health", "/classify", "/sample-feed", "/docs"],
    }


@app.get("/health")
async def health():
    """Simple health check for monitoring."""
    return {"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)}


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest):
    """
    Classify a single news headline as a supply chain disruption signal.

    Request body:
        {"headline": "NH-44 closed near Indore due to flooding"}

    Returns a structured ClassifyResponse with signal type, severity,
    affected corridors, and recommended action — generated by Gemini.
    """
    log.info(f"Classifying headline: {req.headline[:80]}...")

    result = await call_gemini(req.headline, req.region)

    # Build response with safe defaults if any field is missing
    response = ClassifyResponse(
        headline=req.headline,
        signal_type=result.get("signal_type", "other"),
        severity=result.get("severity", "medium"),
        affected_corridors=result.get("affected_corridors", []),
        suggested_action=result.get("suggested_action", "Monitor situation"),
        confidence=float(result.get("confidence", 0.7)),
        reasoning=result.get("reasoning", "Classified by Gemini."),
    )

    log.info(f"Classified as {response.signal_type} / {response.severity}")
    return response


@app.get("/sample-feed")
async def sample_feed():
    """
    Returns the pre-configured Indian news headlines used for demos.
    Frontend can pick one randomly to send to /classify.
    """
    return {
        "count": len(SAMPLE_HEADLINES),
        "headlines": SAMPLE_HEADLINES,
        "region": "India",
        "note": "Curated real Indian supply chain headlines for demo reliability."
    }


# ---- Local dev entrypoint ----

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
