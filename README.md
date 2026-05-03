# Wiki Quiz Generator (Deepklarity Assignment)

This project implements the full assignment:
- FastAPI backend
- PostgreSQL persistence
- Wikipedia HTML scraping with BeautifulSoup
- LLM-based quiz generation through LangChain (Gemini free tier compatible)
- Two-tab frontend (Generate Quiz + Past Quizzes with Details modal)

## Features

### Tab 1 - Generate Quiz
- Accepts a Wikipedia article URL
- Scrapes article title, summary, sections, and entities
- Generates quiz questions (question, 4 options, answer, difficulty, explanation)
- Suggests related topics
- Stores result in PostgreSQL
- Returns structured JSON

### Tab 2 - Past Quizzes
- Lists all generated quiz entries from DB
- Opens full quiz details in modal

## Tech Stack

- Backend: `FastAPI`
- DB: `PostgreSQL` + `SQLAlchemy`
- Scraping: `requests` + `BeautifulSoup`
- LLM: `LangChain` + `Gemini` (`langchain-google-genai`)
- Frontend: minimal HTML/CSS/JS

## Setup

1. Start PostgreSQL:
   ```bash
   docker compose up -d
   ```

2. Create and activate virtual env:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   ```
   Add `GOOGLE_API_KEY` for real LLM generation.
   If missing, the app uses a deterministic fallback quiz generator.

5. Run app:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

6. Open in browser:
   - [http://127.0.0.1:8000](http://127.0.0.1:8000)

## API Endpoints

- `POST /api/quizzes/generate`
  - Request:
    ```json
    { "url": "https://en.wikipedia.org/wiki/Alan_Turing" }
    ```
  - Response: full generated + extracted quiz payload.

- `GET /api/quizzes`
  - Returns quiz history for Tab 2 table.

- `GET /api/quizzes/{id}`
  - Returns full details for one quiz.

## Prompt Template

Prompt template used for generation is in:
- `backend/app/services/prompts.py`

## Sample Data

- Tested URLs: `sample_data/tested_urls.txt`
- Sample API output: `sample_data/sample_api_output.json`

## Notes on Assignment Deliverables

- Quiz generation page, history view, and details modal are implemented.
- You can capture screenshots after running the app.
