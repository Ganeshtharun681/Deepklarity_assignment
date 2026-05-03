from sqlalchemy import JSON, Column, DateTime, Integer, String, Text, func

from .database import Base


class QuizRecord(Base):
    __tablename__ = "quiz_records"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1024), nullable=False, unique=True, index=True)
    title = Column(String(512), nullable=False)
    summary = Column(Text, nullable=False)
    key_entities = Column(JSON, nullable=False)
    sections = Column(JSON, nullable=False)
    quiz = Column(JSON, nullable=False)
    related_topics = Column(JSON, nullable=False)
    raw_html = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
