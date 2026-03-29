# 🤖 Meeting-to-Execution Autopilot

> **Unstop GenAI Hackathon 2026 — Agentic AI Track**  
> *Autonomous multi-agent system that converts meeting transcripts into tracked, self-correcting enterprise workflows — zero human clicks required.*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2016-black?style=flat&logo=next.js)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-4285F4?style=flat&logo=google)](https://deepmind.google/technologies/gemini/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python)](https://python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org/)

---

## What It Does

A meeting ends. Decisions were made. Things were assigned. And then — usually — half of them fall through the cracks.

**AutopilotOS** eliminates that gap. It ingests a meeting transcript (typed, pasted, or spoken live via browser microphone), runs it through a **7-agent autonomous pipeline**, and produces structured tasks with owners, priorities, risk levels, and deadlines — all tracked, self-corrected, and immutably logged.

### The Pipeline: 7 Specialized Agents

| # | Agent | Responsibility |
|---|---|---|
| ① | **Extractor Agent** | Calls Gemini 2.5 Flash with structured JSON output to parse decisions, owners, priorities, and risk levels from raw transcript |
| ② | **Orchestrator Agent** | Maps extracted JSON into database task entities; evaluates dependencies |
| ③ | **Owner Assignment Agent** | Infers owner via role heuristics when transcript doesn't name one; flags for human review |
| ④ | **Health Monitor Agent** | Scans for SLA breaches and stalled tasks (cron-based in production) |
| ⑤ | **Recovery + Escalation Agent** | Self-corrects: bumps priority for low-risk stalls; escalates high-risk tasks to VP |
| ⑥ | **Verification Agent** | Fires when a task is marked complete — logs a signed verification with confidence score |
| ⑦ | **Audit Trail Agent** | Append-only immutable ledger: every agent action, timestamp, confidence, and human-review flag |

---

## Demo Screenshots

> Start the app locally and navigate to `http://localhost:3000`.

| Dashboard | Task Kanban | Audit Trail |
|---|---|---|
| Live metrics + at-risk predictor | Task cards with status + risk | Full agent decision timeline |

---

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full system diagram, agent communication patterns, error-handling logic, and tool integration map.

```
Browser / Webhook
      │
      ▼  POST /meetings
 FastAPI Backend  ←→  Next.js Frontend (REST)
      │
      ▼  Background Task
 Extractor Agent  →  Gemini 2.5 Flash (Structured JSON)
      │
      ▼
 Orchestrator Agent  →  SQLite (tasks)
      │
      ├→  Owner Assignment Agent (if owner == null)
      │
      ▼  Cron / Manual Trigger
 Health Monitor  →  Recovery / Escalation Agent  →  [Slack / Jira adapters]
      │
      ▼  On task completion
 Verification Agent
      │
      ▼  (every step)
 Audit Trail Agent  →  SQLite (audit_logs)
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS v4 |
| **Backend** | FastAPI, Python 3.12, Pydantic v2, SQLAlchemy |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **AI / LLM** | Google Gemini 2.5 Flash (`google-genai` SDK, structured JSON output) |
| **Dev Tools** | Uvicorn, python-dotenv, APScheduler |

---

## Project Structure

```
meeting-execution-autopilot/
├── backend/
│   ├── agents/
│   │   ├── extractor.py        # Gemini 2.5 Flash extraction + fallback mock
│   │   ├── orchestrator.py     # Task creation + Owner Assignment Agent
│   │   ├── monitor.py          # Health Monitor Agent
│   │   ├── recovery.py         # Recovery + Escalation Agent
│   │   ├── verification.py     # Verification Agent
│   │   └── audit.py            # Audit Trail Agent (append-only logger)
│   ├── routers/
│   │   ├── meetings.py         # POST /meetings → triggers pipeline
│   │   ├── tasks.py            # CRUD + /at-risk + /trigger-health-monitor
│   │   ├── approvals.py        # Human approval queue
│   │   ├── audit.py            # GET /audit
│   │   └── demo.py             # Seed / Reset / Scenario runner
│   ├── main.py                 # FastAPI app + CORS + router registration
│   ├── models.py               # SQLAlchemy models: Meeting, Task, AuditLog
│   ├── schemas.py              # Pydantic response schemas
│   ├── database.py             # SQLAlchemy engine + session factory
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Main dashboard (metrics, at-risk, tasks)
│   │   ├── meetings/           # Meeting ingestion + live microphone
│   │   ├── tasks/              # Task management view
│   │   ├── approvals/          # Human approval queue UI
│   │   ├── audit/              # Audit trail timeline
│   │   ├── demo/               # Demo scenario runner
│   │   └── team/[name]/        # Team member view
│   ├── components/             # Reusable UI components
│   ├── lib/api.ts              # Typed REST client for FastAPI
│   └── package.json
├── docs/
│   ├── architecture.md         # System diagram + agent roles
│   ├── impact-model.md         # Quantified ROI model
│   ├── demo-runbook.md         # 3-minute live demo script
│   └── pitch-script.md         # Hackathon pitch narrative
└── docker-compose.yml
```

---

## Setup Instructions

### Prerequisites

| Tool | Minimum Version |
|---|---|
| Python | 3.11+ |
| Node.js | 18+ |
| npm | 9+ |

A **Gemini API key** is optional — the system falls back to deterministic mock data automatically if no key is provided.

---

### Option A — Local Development (Recommended)

#### 1. Clone the repository

```bash
git clone https://github.com/aryankushwaha007/Meetin-Executin-autopilot.git
cd Meetin-Executin-autopilot
```

#### 2. Backend setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure environment (optional — for live Gemini AI)

```bash
# Create a .env file in the backend/ directory
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

> **No API key?** The system works fully without one. The Extractor Agent falls back to a keyword-based mock that produces realistic task data for demo purposes.

#### 4. Start the backend

```bash
uvicorn main:app --reload
```

Backend is running at → **`http://localhost:8000`**  
Interactive API docs → **`http://localhost:8000/docs`**

#### 5. Frontend setup (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Dashboard is running at → **`http://localhost:3000`**

---

### Option B — Docker Compose

```bash
# From the repository root
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend Dashboard | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Running the Demo

Once both services are running, follow the **3-minute demo script** in [`docs/demo-runbook.md`](docs/demo-runbook.md):

1. **Open** `http://localhost:3000`
2. **Go to** the *Demo Runner* tab → click **"Wipe & Seed Database"** to load sample data
3. **Go to** the *Meetings* tab → paste a transcript → click **"Send to Pipeline"**
4. **Watch** tasks auto-populate with owners, priorities, and risk levels
5. **Go to** the *Demo Runner* tab → click **"Run Health Monitor + Recovery"**
6. **Observe** the Security Audit task auto-escalate to VP of Engineering
7. **Go to** the *Audit Trail* tab → review the immutable agent decision log

---

## Key API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/meetings/` | Submit transcript → triggers full agent pipeline |
| `GET` | `/tasks/` | List all tasks |
| `GET` | `/tasks/at-risk` | Bottleneck prediction — tasks predicted to breach SLA |
| `POST` | `/tasks/trigger-health-monitor` | Manually fire the Health Monitor + Recovery agents |
| `PUT` | `/tasks/{id}/status` | Update task status (triggers Verification Agent on `completed`) |
| `GET` | `/approvals/pending` | Fetch tasks awaiting human review |
| `POST` | `/approvals/{id}/resolve` | Approve or reject a low-confidence extraction |
| `GET` | `/audit/` | Full immutable audit log |
| `POST` | `/demo/seed` | Seed database with sample data |
| `POST` | `/demo/reset` | Wipe all data for fresh demo |

---

## Business Impact

See [`docs/impact-model.md`](docs/impact-model.md) for the full quantified model. Summary for a 100-person organization:

| Value Stream | Annual Savings |
|---|---|
| Manual follow-up time eliminated | $168,750 |
| SLA breach prevention via Recovery Agent | $460,800 |
| Compliance audit labor saved | $37,100 |
| Escalation response acceleration | $108,000 |
| **Total Annual ROI** | **$774,650** |

> At $36,000/yr (Growth tier): **ROI = 2,051% · Payback period = ~17 days**

---

## Documentation Index

| Document | Purpose |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | System diagram, agent roles, error-handling logic, tool integrations |
| [`docs/impact-model.md`](docs/impact-model.md) | Quantified business ROI with full assumptions |
| [`docs/demo-runbook.md`](docs/demo-runbook.md) | Click-by-click 3-minute live demo script |
| [`docs/pitch-script.md`](docs/pitch-script.md) | Hackathon pitch narrative |

---

## What's Not Included (Intentionally)

| Excluded Item | Reason |
|---|---|
| `.env` files | Contains API keys — use `.env.example` pattern instead |
| `backend/venv/` | Regenerated via `pip install -r requirements.txt` |
| `frontend/node_modules/` | Regenerated via `npm install` |
| `frontend/.next/` | Build artifact |
| `backend/autopilot.db` | Runtime database — created fresh on first launch |
| `*.tsbuildinfo` | TypeScript incremental build cache |

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built for the Unstop GenAI Hackathon 2026 · AutopilotOS v1.0*
