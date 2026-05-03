QUIZ_PROMPT_TEMPLATE = """
You are generating a quiz from a Wikipedia article.
Use only facts from the article text below.

ARTICLE TITLE: {title}
ARTICLE SUMMARY: {summary}
ARTICLE SECTIONS: {sections}
ARTICLE TEXT:
{article_text}

Return valid JSON with this schema:
{{
  "quiz": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": "one option exactly",
      "difficulty": "easy|medium|hard",
      "explanation": "brief factual explanation"
    }}
  ],
  "related_topics": ["topic1", "topic2", "topic3"]
}}

Rules:
- Generate {question_count} questions.
- Exactly 4 options per question.
- Ensure answer is present in options.
- Include a mix of easy, medium, and hard when possible.
- No hallucinations or external facts.
"""
