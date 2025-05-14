# app/crud/news_article.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.news_article import NewsArticle
from app.schemas.news_article import NewsArticleCreate

async def create_news_article(db: AsyncSession, news: NewsArticleCreate) -> NewsArticle:
    db_news = NewsArticle(**news.dict())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

async def get_news_article(db: AsyncSession, news_id: int) -> NewsArticle | None:
    result = await db.execute(select(NewsArticle).where(NewsArticle.id == news_id))
    return result.scalars().first()

async def get_news_articles(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[NewsArticle]:
    result = await db.execute(select(NewsArticle).offset(skip).limit(limit))
    return result.scalars().all()
