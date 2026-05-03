import json
import random

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from ..config import settings
from .prompts import QUIZ_PROMPT_TEMPLATE

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:  # pragma: no cover
    ChatGoogleGenerativeAI = None


def _fallback_quiz(article: dict, question_count: int) -> dict:
    summary = article["summary"]
    section_pool = article["sections"] or ["Overview", "Background", "Impact"]
    seed_options = [
        "Historical impact",
        "Biographical details",
        "Scientific contribution",
        "Social context",
        "Technical methodology",
        "Institutional collaboration",
    ]
    difficulties = ["easy", "medium", "hard"]
    quiz = []
    for i in range(question_count):
        section = section_pool[i % len(section_pool)]
        options = random.sample(seed_options, 4)
        answer = options[0]
        quiz.append(
            {
                "question": f"Which theme is most connected to the '{section}' part of {article['title']}?",
                "options": options,
                "answer": answer,
                "difficulty": difficulties[i % len(difficulties)],
                "explanation": f"This is inferred from the article summary: {summary[:120]}...",
            }
        )
    return {"quiz": quiz, "related_topics": section_pool[:5]}


def generate_quiz_with_llm(article: dict, question_count: int = 6) -> dict:
    if not settings.google_api_key or ChatGoogleGenerativeAI is None:
        return _fallback_quiz(article, question_count)

    prompt = PromptTemplate.from_template(QUIZ_PROMPT_TEMPLATE)
    model = ChatGoogleGenerativeAI(
        model=settings.llm_model,
        google_api_key=settings.google_api_key,
        temperature=0.3,
    )
    chain = prompt | model | StrOutputParser()
    raw = chain.invoke(
        {
            "title": article["title"],
            "summary": article["summary"],
            "sections": ", ".join(article["sections"]),
            "article_text": article["article_text"],
            "question_count": question_count,
        }
    )

    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json\n", "", 1).strip()

    parsed = json.loads(cleaned)
    if "quiz" not in parsed or "related_topics" not in parsed:
        raise ValueError("LLM response missing required fields.")
    return parsed
