import re

import requests
from bs4 import BeautifulSoup

from ..config import settings


def _extract_entities(text: str) -> dict:
    people = sorted(set(re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", text)))[:12]
    org_keywords = ("University", "Institute", "Company", "Park", "Laboratory", "College")
    organizations = sorted({item for item in people if any(k in item for k in org_keywords)})[:10]
    locations = sorted(
        set(
            re.findall(
                r"\b(?:United Kingdom|United States|India|Germany|France|London|Paris|Cambridge|Oxford)\b",
                text,
            )
        )
    )[:10]
    return {
        "people": people[:10],
        "organizations": organizations,
        "locations": locations,
    }


def scrape_wikipedia(url: str) -> dict:
    if "wikipedia.org/wiki/" not in url:
        raise ValueError("Please provide a valid Wikipedia article URL.")

    headers = {"User-Agent": "WikiQuizGenerator/1.0 (contact@example.com)"}
    response = requests.get(url, headers=headers, timeout=settings.request_timeout_seconds)
    response.raise_for_status()
    raw_html = response.text

    soup = BeautifulSoup(raw_html, "html.parser")
    title = (soup.find("h1", id="firstHeading") or soup.find("title")).get_text(strip=True)
    title = title.replace(" - Wikipedia", "")

    content_root = soup.find("div", id="mw-content-text")
    if not content_root:
        raise ValueError("Could not locate article content on this page.")

    paragraphs = [
        p.get_text(" ", strip=True)
        for p in content_root.select("p")
        if p.get_text(" ", strip=True)
    ]
    if not paragraphs:
        raise ValueError("Article text is empty or unavailable.")

    summary = paragraphs[0]
    article_text = "\n".join(paragraphs)[: settings.max_article_chars]
    sections = [
        h.get_text(" ", strip=True)
        for h in content_root.select("h2 .mw-headline, h3 .mw-headline")
        if h.get_text(" ", strip=True) and "References" not in h.get_text(" ", strip=True)
    ][:20]

    entities = _extract_entities(article_text)
    return {
        "url": url,
        "title": title,
        "summary": summary,
        "sections": sections,
        "article_text": article_text,
        "key_entities": entities,
        "raw_html": raw_html,
    }
