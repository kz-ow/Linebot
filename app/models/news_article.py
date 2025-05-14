# app/models/news_article.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class NewsArticle(Base):
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1024), nullable=True)
    source = Column(String(255), nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow)
