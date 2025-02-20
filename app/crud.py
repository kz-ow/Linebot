# app.crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import NewsArticle, User
from app.schemas import NewsArticleCreate, UserCreate

async def create_new_article(db: AsyncSession, news: NewsArticleCreate) -> NewsArticle:
    db_news = NewsArticle(**news.dict())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

async def get_news_article(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[NewsArticle]:
    result = await db.execute(select(NewsArticle).offset(skip).limit(limit))
    return result.scalars().all()

async def update_news_article(db: AsyncSession, news_id: int, news: NewsArticleCreate) -> NewsArticle | None:
    db_news = await get_news_article(db, news_id)
    if db_news is None:
        return None
    for key, value in news.dict(exclude_unset=True).items():
        setattr(db_news, key, value)
    await db.commit()
    await db.refresh(db_news)
    return db_news

async def delete_news_article(db: AsyncSession, news_id: int):
    db_news = await get_news_article(db, news_id)
    if db_news is None:
        return False
    await db.delete(db_news)
    await db.commit()
    return True

# ==============================================================
# User用

async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_line_id(db: AsyncSession, line_id: str) -> User | None:
    result = await db.execute(select(User).where(User.line_id == line_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return result.scalars().all()

async def update_user_subscription_status(db: AsyncSession, line_id: str, subscribe: bool) -> User | None:
    user = await db.execute(select(User).where(User.line_id == line_id))
    if user is None:
        print(None)
    user.is_subscribed = subscribe
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_interests(db: AsyncSession, line_id: str, intersts: str) -> User | None:
    user = await get_user_by_line_id(db, line_id)
    if user is None:
        return None
    user.interests = intersts
    await db.commit()
    await db.refresh(user)
    return user
