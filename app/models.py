# app/model.py
from sqlalchemy import Column, Integer, String, Text, Datetime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

#ニュース記事を保存するモデル
class NewsArticle(Base):
    __tabelname__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(1024), nullable=True)
    source = Column(String(255), nullable=True)
    published_at = Column(Datetime, default=datetime.utcnow)

class User(Base):
    __tabelname__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(String(255), unique=True)
    is_subscribed = Column(Boolean, default=True)

    interests = Column(Text, nullable=True)
