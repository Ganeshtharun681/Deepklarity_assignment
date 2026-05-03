from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Wiki Quiz Generator"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/wiki_quiz"
    google_api_key: str | None = None
    llm_model: str = "gemini-1.5-flash"
    request_timeout_seconds: int = 30
    max_article_chars: int = 12000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
