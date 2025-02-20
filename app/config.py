# app/config.py
from pydantic import BaseSettings # setting用のライブラリ

class Settings(BaseSettings):
    
    LINE_CHANNEL_SECRET: str
    LINE_CHANNEL_ACCESS_TOEKN: str

    NEWS_API_KEY: str
    NEWS_API_URL: str = "https://newsapi.prg/v2/top-headlines"
    LINENEWS_RSS_URL: str = "https://news.line.me/rss"

    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()