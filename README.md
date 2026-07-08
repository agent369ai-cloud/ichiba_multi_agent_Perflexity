# Ichiba Merchant Support Assistant (IMSA)

A prototype multi-agent merchant support assistant built with FastAPI and a LangGraph-based agent workflow. It accepts merchant queries and routes them across agents for planning, RAG, SQL/API retrieval, synthesis, and guardrail review.

## Features

- FastAPI backend with `/ask` support endpoint
- Pydantic request/response validation
- Modular agent graph pipeline defined in `graph_flow.py`
- Includes router, planner, memory, RAG, SQL, API, synthesizer, critic, and guardrail agents
- Configurable model and OpenAI API key via environment variables

## Requirements

- Python 3.11+
- `venv` or other virtual environment
- OpenAI API key

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set the OpenAI API key:

```powershell
$env:OPENAI_API_KEY = "your_openai_api_key"
```

## Configuration

The app uses `config.py` for the following settings:

- `OPENAI_API_KEY` - OpenAI API key
- `MODEL_NAME` - default `gpt-4o-mini`
- `ENV` - environment mode

## Run

Start the app with Uvicorn:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Then open:

- Health check: `http://127.0.0.1:8000/`
- Support endpoint: `http://127.0.0.1:8000/ask`

## API

### POST /ask

Request body:

```json
{
  "merchant_id": "merchant-123",
  "language": "en",
  "query": "How can I resolve a billing issue?",
  "session_id": "session-abc"
}
```

Response body:

```json
{
  "merchant_id": "merchant-123",
  "query": "How can I resolve a billing issue?",
  "route": "...",
  "plan": ["..."],
  "evidence": [
    {
      "source": "...",
      "source_type": "...",
      "confidence": 0.9,
      "content": "...",
      "metadata": {}
    }
  ],
  "final_answer": "...",
  "status": "success"
}
```

## Project structure

- `app.py` — FastAPI app entrypoint
- `config.py` — application settings
- `models.py` — request/response and evidence models
- `graph_flow.py` — agent workflow graph definition
- `agents.py` — agent implementations (router, planner, memory, RAG, SQL, API, synthesizer, critic, guardrail)
- `requirements.txt` — Python dependencies
- `SampleRequest01.JSON`, `SampleRequest02.JSON` — sample requests

## Notes

This is a proof-of-concept repository. You should secure API keys and validate external agent integrations before production use.

## Contributing

Contributions are welcome. Please see `CONTRIBUTING.md` for guidelines on reporting issues, submitting pull requests, and preparing code changes.

