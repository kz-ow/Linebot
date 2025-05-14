# app/schemas/news_article.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticleBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    source: Optional[str] = None

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticleOut(NewsArticleBase):
    id: int
    published_at: datetime

    class Config:
        orm_mode = True
