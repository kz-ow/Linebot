# app/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOKEN: str
    POSTGRES_URL: str      
    POSTGRES_USER: str     
    POSTGRES_PASSWORD: str 
    GEMINI_API_KEY: str
    GEMINI_REGION: str
    LIFF_ID_DETAIL: str
    LIFF_ID_REGULAR: str
    LIFF_ID_CATEGORY: str
    TAVILY_API_KEY: str

    LANGUAGES: List[str] = (
        "日本語",
        "英語",
        "フランス語",
        "ドイツ語",
        "スペイン語",
        "韓国語",
        "中国語",
        "ロシア語"
    )

    class Config:
        env_file = ".env"
        from_attributes = True

settings = Settings()
