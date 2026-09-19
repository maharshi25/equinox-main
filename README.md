# Equinox

Equinox is an AI-powered life operating system built to help people balance health, focus, and productivity with one intelligent workflow.

It combines personal context, wellness data, task management, and AI-powered guidance into a single system that helps users act with better clarity instead of more effort.

<div align="center">

[![Live demo](https://img.shields.io/badge/Live%20Demo-equinox0.netlify.app-blue?style=for-the-badge)](https://equinox0.netlify.app)
[![Observability](https://img.shields.io/badge/Observability-Opik-orange?style=for-the-badge)](https://www.comet.com/opik)
[![AI stack](https://img.shields.io/badge/AI-LangChain-green?style=for-the-badge)](https://langchain.com)

</div>

---

## Why Equinox

Most people juggle too many disconnected systems:

- health and sleep data
- task lists and reminders
- email and communication
- calendars and commitments

Equinox brings those inputs together so decisions can be based on actual energy, focus, and workload rather than fragmentation.

---

## What it does

### Health-aware planning

The wellness agent evaluates sleep, recovery, stress, and energy to guide sustainable work patterns.

### Intelligent coordination

A supervisor agent routes user requests to the right specialist and coordinates decisions across health, productivity, and communication.

### Productivity support

The productivity layer manages notes, tasks, and email-related actions in the same decision context.

### Daily briefing

Users receive a concise briefing with readiness signals, important tasks, and helpful summaries before the day starts.

---

## Architecture

### Multi-agent workflow

| Agent              | Purpose                                              |
| ------------------ | ---------------------------------------------------- |
| Supervisor         | Routes requests and coordinates decisions            |
| Wellness Agent     | Tracks readiness, recovery, and daily health context |
| Productivity Agent | Handles tasks, notes, and work-related operations    |
| Briefing Agent     | Creates summaries and daily guidance                 |

### Observability

Every major AI interaction is traced with Opik so prompts, tool calls, and model decisions remain visible and debuggable.

### Security and access control

Equinox uses JWT-based authentication for protected user actions and thread access. Sensitive chat history endpoints validate the signed-in user before allowing reads or updates, helping keep each account scoped to its own data.

---

## Tech stack

### Backend

- FastAPI
- LangChain + LangGraph
- Groq LLMs
- PostgreSQL
- Google OAuth 2.0
- JWT-based access control for authenticated sessions
- Opik tracing

### Frontend

- React + TypeScript
- Vite
- React Router
- React Markdown

---

## Quick start

### 1) Clone the repo

```bash
git clone https://github.com/maharshi25/equinox-main.git
cd equinox-main
```

### 2) Configure environment variables

Create `backend/.env` with values like:

```env
GROQ_API_KEY=your_groq_api_key
OPIK_API_KEY=your_opik_api_key
OPIK_WORKSPACE=your_opik_workspace
OPIK_PROJECT_NAME=equinox
DATABASE_URL=postgresql://user:pass@localhost:5432/equinox
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 3) Install dependencies

```bash
cd backend
pip install -r requirements.txt

cd ../frontend
npm install
```

### 4) Run the app

```bash
cd ..
chmod +x startup.sh
./startup.sh
```

---

## Project structure

```text
equinox-main/
├── backend/
│   ├── agents/
│   ├── api/
│   ├── database/
│   ├── state/
│   ├── tools/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
├── startup.sh
├── README.md
├── .gitignore
└── package-lock.json
```

---

## Core API overview

### Todos

| Method   | Endpoint         | Description    |
| -------- | ---------------- | -------------- |
| `GET`    | `/todos/{email}` | Get user todos |
| `POST`   | `/todos/`        | Create a todo  |
| `PATCH`  | `/todos/{id}`    | Update a todo  |
| `DELETE` | `/todos/{id}`    | Delete a todo  |

### Notes

| Method   | Endpoint         | Description    |
| -------- | ---------------- | -------------- |
| `GET`    | `/notes/{email}` | Get user notes |
| `POST`   | `/notes/`        | Create a note  |
| `PATCH`  | `/notes/{id}`    | Update a note  |
| `DELETE` | `/notes/{id}`    | Delete a note  |

### Chat history

| Method | Endpoint                           | Description                  |
| ------ | ---------------------------------- | ---------------------------- |
| `GET`  | `/api/history/{email}`             | Get all conversation threads |
| `GET`  | `/api/history/{email}/{thread_id}` | Get a specific thread        |
| `POST` | `/api/history/{email}/{thread_id}` | Save a thread                |

---

## Opik integration

Equinox uses Opik for LLM observability and debugging.

### Tracked details

- agent invocations
- tool calls
- prompt and response traces
- latency and token usage
- thread-based conversation tracking

### View traces

1. Visit [comet.com/opik](https://www.comet.com/opik)
2. Open the `equinox` project
3. Inspect traces grouped by `thread_id`

---

## Why it matters

The future of productivity is not more apps — it is better context and better decisions.

Equinox is designed to help people work with their energy rather than against it, combining personal awareness and AI support into a more sustainable system.

---

## License

This project is intended for demonstration and development use. Review your target deployment and licensing requirements before commercial use.

### Why Opik?

- **Debug AI issues** — See exactly what the LLM received and responded
- **Optimize costs** — Monitor token usage across agents
- **Improve quality** — Analyze agent decisions and tool usage

---

## 🧪 Development

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🐛 Troubleshooting

| Issue                         | Solution                                             |
| ----------------------------- | ---------------------------------------------------- |
| `OPIK_API_KEY not found`      | Set in `backend/.env`                                |
| Google OAuth errors           | Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` |
| Rate limiting (429)           | Groq free tier: 30 req/min. Wait or upgrade.         |
| Database connection errors    | Verify `DATABASE_URL` and PostgreSQL is running      |
| Briefing shows 0 emails/tasks | Re-authenticate with Google OAuth                    |

---

## 👨‍💻 Author

**Maharshi Shukla**

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**🌅 Equinox — Balance your day with AI**

</div>
