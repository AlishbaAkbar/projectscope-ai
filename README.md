# ProjectScope AI — Week 1 Prototype

> **AI-Powered Software Requirement Analysis & Scoping Engine**
> 
> *Week 1 Prototype: Requirement Analyzer, Pydantic Validation, Canonical Feature Normalizer & Deterministic Task Generator.*

---

## 1. Overview & Prototype Scope

**ProjectScope AI** is an AI-powered SaaS platform that converts natural-language software project briefs or idea descriptions into structured, validated software development plans.

### Week 1 Pipeline

```text
User Project Idea
       ↓
FastAPI Backend (/api/v1/projects/{id}/analyze)
       ↓
Requirement Analyzer (Prompt Engine + LLM Provider: Gemini / OpenAI / Mock)
       ↓
Raw AI Output (JSON)
       ↓
Pydantic Validation & Error Recovery
       ↓
Feature Normalizer (Canonical Dictionary Mapping)
       ↓
Deterministic Task Generator (Role / Discipline Breakdown)
       ↓
Relational Storage (SQLite / PostgreSQL)
       ↓
Interactive Dashboard (Next.js TypeScript Frontend)
```

> [!NOTE]
> This repository represents the **Week 1 Working Prototype**. Advanced ML effort estimation models (XGBoost / Random Forest), vector RAG, billing/subscriptions, microservices, and mobile applications are intentionally out of scope for this phase.

---

## 2. Technology Stack

### Backend
* **Python 3.10+ / 3.14**
* **FastAPI**: Asynchronous high-performance REST framework
* **Pydantic v2**: Strict schema validation and data integrity enforcement
* **SQLAlchemy 2.0**: Relational ORM supporting SQLite & PostgreSQL
* **HTTPX**: Async HTTP client for AI provider REST calls
* **Pytest & Pytest-Asyncio**: Comprehensive test suite

### AI Abstraction
* **Provider Interface**: Pluggable abstraction supporting **Google Gemini**, **OpenAI**, and **Mock Provider** (for offline testing & local zero-cost development).
* **Deterministic Guardrails**: LLMs are never used as a source of truth for arithmetic or deterministic calculations.

### Frontend
* **Next.js 14** (App Router)
* **React 18 & TypeScript**
* **Tailwind CSS & Lucide Icons**

---

## 3. Repository Structure

```text
projectscope-ai/
├── frontend/                     # Next.js TypeScript Web Application
│   ├── src/
│   │   ├── app/                  # App Router (page.tsx, layout.tsx, globals.css)
│   │   ├── components/           # Navbar, Footer, ProjectInputForm, AnalysisResults, etc.
│   │   ├── api/                  # Typed HTTP Client
│   │   └── types/                # TypeScript Interfaces
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── backend/                      # FastAPI Python Application
│   ├── app/
│   │   ├── main.py               # FastAPI entrypoint & middleware
│   │   ├── api/routes/           # REST endpoints (/api/v1/projects)
│   │   ├── ai/
│   │   │   ├── providers/        # LLM Providers (Gemini, OpenAI, Mock, Factory)
│   │   │   ├── prompts/          # Requirements Prompt Template
│   │   │   └── analyzer.py       # Validation & Retry Orchestrator
│   │   ├── schemas/              # Pydantic Schemas (Project, Features, Requirements, Analysis)
│   │   ├── services/             # ProjectService, FeatureService, TaskService
│   │   ├── models/               # SQLAlchemy ORM Models
│   │   ├── database/             # DB Connection & Session Factory
│   │   └── utils/                # Config & Error Handlers
│   └── requirements.txt
│
├── tests/                        # Automated Pytest Suite
│   ├── conftest.py               # In-memory test fixtures
│   ├── test_api.py               # API CRUD & Analyze tests
│   ├── test_ai_validation.py     # Schema validation & error recovery tests
│   ├── test_feature_normalization.py # Keyword-to-Canonical tests
│   ├── test_task_generation.py   # Baseline task generation tests
│   └── test_e2e_projects.py      # E2E test on 4 canonical project scenarios
│
├── prompts/
│   └── requirement_analysis_prompt.txt # Prompt specification
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## 4. Quick Start & Setup Instructions

### Prerequisites
* **Python 3.10+**
* **Node.js 18+ & npm**
* (Optional) **Docker & Docker Compose**

---

### Step 1: Backend Setup

1. Open a terminal in the root directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create your `.env` configuration:
   ```bash
   cp ../.env.example .env
   ```
   *(By default, `AI_PROVIDER=mock` and `DATABASE_URL=sqlite:///./projectscope.db`, so the backend works immediately offline without external API keys).*

4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

5. Access interactive API documentation:
   * **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   * **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Step 2: Frontend Setup

1. Open a new terminal in the `frontend` directory:
   ```bash
   cd frontend
   npm install
   ```

2. Start the Next.js development server:
   ```bash
   npm run dev
   ```

3. Open your browser at [http://localhost:3000](http://localhost:3000).

---

### Step 3: Running via Docker Compose (Optional)

```bash
docker-compose up --build
```
* Frontend will be accessible on `http://localhost:3000`
* Backend will be accessible on `http://localhost:8000`

---

## 5. API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/projects` | Create a new project record |
| `GET` | `/api/v1/projects` | List all projects with pagination |
| `GET` | `/api/v1/projects/{id}` | Get details of a single project |
| `POST` | `/api/v1/projects/{id}/analyze` | **Main Endpoint**: Execute AI requirement analysis, validation, normalization, and task generation |
| `GET` | `/api/v1/projects/{id}/features` | Retrieve extracted features and nested development tasks |
| `GET` | `/api/v1/projects/{id}/tasks` | Retrieve all generated tasks for a project |
| `GET` | `/health` | Server healthcheck and active AI provider info |

---

## 6. AI Requirement Analysis Pipeline

### System Prompt & Extraction Schema

When `/api/v1/projects/{id}/analyze` is invoked:
1. The **RequirementAnalyzer** formats the input description using an expert architect prompt.
2. The active **LLMProvider** produces JSON adhering to the strict schema:
   * `project_type`: Domain categorization (`transportation`, `e-commerce`, `healthcare`, etc.)
   * `users`: Target personas (e.g. `student`, `driver`, `admin`)
   * `requirements`: Atomic statements with `category` and `confidence` (0.0 to 1.0)
   * `features`: Modules with `name`, `description`, `priority`, `complexity`, and `confidence`
   * `missing_information`: Critical questions and ambiguities
   * `assumptions`: Explicit technical/operational assumptions
3. **Pydantic Validation**: Ensures non-empty data and valid types. If malformed, retries with targeted error feedback.
4. **Feature Normalization**: Maps feature names (e.g. `"login"`, `"sign in"`, `"user authentication"`) to canonical domain keys (e.g. `AUTHENTICATION`).
5. **Deterministic Task Generation**: Generates baseline engineering tasks categorized by **Frontend**, **Backend**, **Database**, **QA**, and **Integration** with estimated hours.

---

## 7. Example Analysis

### Example Input
```json
{
  "name": "University Transport App",
  "platform": "Mobile",
  "description": "I want to build a university transport app where students can view buses, track their bus live, receive notifications and report transport issues."
}
```

### Example Structured Output (`POST /api/v1/projects/{id}/analyze`)
```json
{
  "project": {
    "id": 1,
    "name": "University Transport App",
    "description": "I want to build a university transport app where students can view buses, track their bus live, receive notifications and report transport issues.",
    "platform": "Mobile",
    "project_type": "transportation",
    "target_users": ["student", "driver", "transport_admin"]
  },
  "project_type": "transportation",
  "users": ["student", "driver", "transport_admin"],
  "requirements": [
    {
      "id": 1,
      "category": "functional",
      "text": "Students should be able to track assigned buses in real-time on a map.",
      "source": "llm_analysis",
      "confidence": 0.94
    },
    {
      "id": 2,
      "category": "non_functional",
      "text": "The platform must ensure location updates latency remains under 3 seconds.",
      "source": "llm_analysis",
      "confidence": 0.88
    }
  ],
  "features": [
    {
      "id": 1,
      "name": "live_tracking",
      "normalized_key": "LIVE_TRACKING",
      "description": "Real-time GPS vehicle location tracking and route mapping",
      "priority": "critical",
      "complexity": "high",
      "confidence": 0.96,
      "tasks": [
        {
          "title": "Build Real-time Map & Tracking UI",
          "category": "Frontend",
          "estimated_hours": 14.0
        },
        {
          "title": "Implement Real-time Telemetry & Location API",
          "category": "Backend",
          "estimated_hours": 16.0
        },
        {
          "title": "Create Geospatial Telemetry Data Model",
          "category": "Database",
          "estimated_hours": 6.0
        },
        {
          "title": "Integrate Mapping & Routing Provider",
          "category": "Integration",
          "estimated_hours": 8.0
        },
        {
          "title": "Test Telemetry Latency & Disconnection Scenarios",
          "category": "QA",
          "estimated_hours": 6.0
        }
      ]
    }
  ],
  "missing_information": [
    "Required map and routing API provider is not specified.",
    "Hardware source for driver GPS telemetry is not defined."
  ],
  "assumptions": [
    "Students will primarily access the service via Mobile and Web browsers.",
    "GPS coordinates will be broadcast via WebSockets or MQTT."
  ],
  "total_tasks_count": 22,
  "total_estimated_hours": 178.0
}
```

---

## 8. Automated Testing

The project includes unit, validation, normalization, task generation, and end-to-end scenario tests.

Run the test suite:
```bash
# In project root
pytest -v
```

### Test Coverage
* **`tests/test_api.py`**: Project CRUD, 404/422 validation, analyze endpoint, features/tasks endpoints.
* **`tests/test_ai_validation.py`**: Pydantic validation of valid JSON, markdown codeblock stripping, malformed JSON recovery, and missing field errors.
* **`tests/test_feature_normalization.py`**: Normalization dictionary mappings (`"login"` -> `AUTHENTICATION`, `"live tracking"` -> `LIVE_TRACKING`, etc.).
* **`tests/test_task_generation.py`**: Deterministic baseline task breakdown verification across Frontend, Backend, Database, QA, and Integration disciplines.
* **`tests/test_e2e_projects.py`**: End-to-end verification for the 4 canonical test cases:
  1. *University Transport App*
  2. *E-Commerce Store*
  3. *Food Delivery App*
  4. *Healthcare Appointment System*

---

## 9. Known Limitations (Week 1 Prototype)

1. **Effort Estimation is Baseline-Template Driven**: Hour estimates are based on industry baseline templates rather than dynamic ML regression models (which will be added in Phase 2).
2. **Deterministic Task Library**: Subtasks are seeded from our modular canonical taxonomy.
3. **Single LLM Call**: The prototype executes a single-pass extraction pipeline with validation retry rather than a multi-agent debate architecture.

---

## 10. Future Roadmap (Week 2+)

* **Week 2**: Machine Learning Effort & Timeline Estimation Engine (XGBoost / Random Forest regression trained on historical software telemetry).
* **Week 3**: RAG & Contextual Document Ingestion (upload PRDs, RFPs, Figma links, or API docs for analysis).
* **Week 4**: Interactive Scope Refinement (conversational requirement tweaking & interactive uncertainty resolution).
* **Week 5**: Exporting to Jira, GitHub Issues, Linear, and Azure DevOps.
