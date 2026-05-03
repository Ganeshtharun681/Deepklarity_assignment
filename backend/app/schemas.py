from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


Difficulty = Literal["easy", "medium", "hard"]


class GenerateQuizRequest(BaseModel):
    url: HttpUrl


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str
    difficulty: Difficulty
    explanation: str


class KeyEntities(BaseModel):
    people: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)


class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: KeyEntities
    sections: list[str]
    quiz: list[QuizQuestion]
    related_topics: list[str]
    created_at: datetime

    class Config:
        from_attributes = True


class QuizHistoryItem(BaseModel):
    id: int
    url: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True
