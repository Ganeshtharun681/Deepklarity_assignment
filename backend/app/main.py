from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import QuizRecord
from .schemas import GenerateQuizRequest, QuizHistoryItem, QuizResponse
from .services.quiz_generator import generate_quiz_with_llm
from .services.scraper import scrape_wikipedia

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wiki Quiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/assets", StaticFiles(directory=frontend_dir), name="assets")


@app.get("/")
def serve_frontend():
    return FileResponse(frontend_dir / "index.html")


def to_quiz_response(record: QuizRecord) -> QuizResponse:
    return QuizResponse(
        id=record.id,
        url=record.url,
        title=record.title,
        summary=record.summary,
        key_entities=record.key_entities,
        sections=record.sections,
        quiz=record.quiz,
        related_topics=record.related_topics,
        created_at=record.created_at,
    )


@app.post("/api/quizzes/generate", response_model=QuizResponse)
def generate_quiz(payload: GenerateQuizRequest, db: Session = Depends(get_db)):
    url = str(payload.url)
    existing = db.execute(select(QuizRecord).where(QuizRecord.url == url)).scalar_one_or_none()
    if existing:
        return to_quiz_response(existing)

    try:
        article = scrape_wikipedia(url)
        generated = generate_quiz_with_llm(article, question_count=6)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f"Generation failed: {exc}") from exc

    record = QuizRecord(
        url=article["url"],
        title=article["title"],
        summary=article["summary"],
        key_entities=article["key_entities"],
        sections=article["sections"],
        quiz=generated["quiz"],
        related_topics=generated["related_topics"],
        raw_html=article["raw_html"],
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc

    return to_quiz_response(record)


@app.get("/api/quizzes", response_model=list[QuizHistoryItem])
def list_quizzes(db: Session = Depends(get_db)):
    rows = db.execute(select(QuizRecord).order_by(QuizRecord.created_at.desc())).scalars().all()
    return rows


@app.get("/api/quizzes/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    record = db.get(QuizRecord, quiz_id)
    if not record:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return to_quiz_response(record)
