# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    NEWS_API_KEY: str
    NEWS_API_URL: str
    POSTGRES_URL: str      
    POSTGRES_USER: str     
    POSTGRES_PASSWORD: str 
    GEMINI_API_KEY: str
    GEMINI_REGION: str
    DEEPL_API_KEY: str
    DEEPL_URL: str = "https://api-free.deepl.com/v2/translate"

    TOPICS: tuple[tuple[str, str], ...] = (
        ("business",      "ビジネス"),
        ("entertainment", "エンタメ"),
        ("general",       "一般"),
        ("health",        "健康"),
        ("science",       "科学"),
        ("sports",        "スポーツ"),
        ("technology",    "テクノロジー"),
    )

    class Config:
        env_file = ".env"
        from_attributes = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
