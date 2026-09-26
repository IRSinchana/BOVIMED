# BOVIMED

**Smart Vision for Healthier Herds**

AI-powered dairy health & early mastitis detection platform.

> **Status:** STEP 1 complete — project structure and toolchains initialized.  
> Full application features will be implemented in subsequent steps.

---

## Project overview

BOVIMED is a web application for dairy farmers that analyzes cow/udder images using a YOLO11 computer vision model to support early mastitis screening, health history, alerts, and recommendations.

This is an **AI-assisted screening** tool — not a substitute for professional veterinary diagnosis.

---

## Tech stack

| Layer | Stack |
|-------|--------|
| Frontend | React, Vite, Tailwind CSS, Lucide React, Recharts |
| Backend | Python, FastAPI, Uvicorn, SQLAlchemy, SQLite |
| AI | Ultralytics YOLO11 (`backend/models/best.pt`) |

---

## Project structure (STEP 1)

```
BOVIMED/
├── frontend/                 # React + Vite app
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── layouts/
│       ├── services/
│       ├── hooks/
│       ├── utils/
│       ├── data/
│       └── assets/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database/
│   │   └── utils/
│   ├── models/               # Place best.pt here
│   ├── uploads/
│   ├── results/
│   ├── requirements.txt
│   └── venv/
├── .env.example
├── .gitignore
└── README.md
```

---

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Webcam (optional, for camera scan feature)

---

## Installation

### 1. Clone / open the project

```bash
cd BOVIMED
```

### 2. Environment file

```bash
copy .env.example .env
```

On macOS/Linux: `cp .env.example .env`

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### 4. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

---

## YOLO11 model setup

Place your trained weights at:

```
backend/models/best.pt
```

Until a real model is present, set `DEMO_MODE=true` in `.env`.  
The UI must clearly show **Demo Mode** when mock inference is used.

---

## Environment variables

See `.env.example` for:

- `DEMO_MODE` — use labeled demo results when `true`
- `MODEL_PATH` — path to YOLO11 weights
- `DATABASE_URL` — SQLite connection string
- `MAX_UPLOAD_SIZE_MB` — upload limit
- `VITE_API_BASE_URL` — frontend → backend URL
- Risk thresholds: `HEALTHY_THRESHOLD`, `MILD_THRESHOLD`, `MODERATE_THRESHOLD`, `SEVERE_THRESHOLD`

---

## Current step

**STEP 1 — Project structure & initialization** ✅  
**STEP 2 — FastAPI backend** ✅

Next (when you say continue): **STEP 3+ frontend / remaining product modules**

### Backend quick test

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs and try `POST /api/analyze` with an image.  
With `DEMO_MODE=true`, responses are explicitly labeled demo. With `DEMO_MODE=false` and `best.pt` present, LIVE YOLO11 is used.

---

## Authentication

JWT bearer tokens. Passwords are hashed with bcrypt (never stored in plaintext).

### Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/logout`
- `PUT /api/auth/profile`
- `POST /api/chat` — Ask BOVIMED (rule-based + optional LLM)
- `GET /api/chat/history`
- `DELETE /api/chat/history`
- `POST /api/veterinarians/search` — never invents contacts

### Demo farmer account (seeded on backend startup)

- Mobile: `9876543210`
- Email: `farmer@bovimed.demo`
- Password: `Demo@1234`

Documented here only — not shown in the UI.

### Frontend routes

- `/login`, `/register`
- Protected: `/dashboard`, `/analyze`, `/camera`, `/cows`, `/history`, `/alerts`, `/chat`, `/veterinarians`, `/settings`, `/result`

### Languages (i18next)

22 scheduled Indian languages in Settings. Full professional UI packs: English, Hindi, Kannada, Telugu (+ strong packs for Tamil and others where present). Missing keys honestly fall back to English via deep-merge + `fallbackLng`.

Urdu / Sindhi / Kashmiri switch `dir="rtl"`.

### Optional environment variables

```
GOOGLE_PLACES_API_KEY=
VET_PROVIDER=
BOVIMED_LLM_API_KEY=
BOVIMED_LLM_ENABLED=false
GEMINI_API_KEY=
OPENAI_API_KEY=
```

Without LLM keys, the chatbot uses a safe local knowledge base. Without Places keys, veterinarian search uses OpenStreetMap when GPS is available, otherwise returns an honest “could not be verified” message and map directions — never fake phone numbers.

---

## Disclaimer

BOVIMED provides AI-assisted screening and care guidance. It is not a veterinary diagnosis and does not replace a qualified veterinarian.
