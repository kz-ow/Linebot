# app/config.py
from pydantic_settings import BaseSettings

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
    LIFF_ID_DETAIL: str
    LIFF_ID_REGULAR: str
    LIFF_ID_CATEGORY: str
    TAVILY_API_KEY: str
    

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

settings = Settings()
