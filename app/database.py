# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# 非同期エンジンの作成
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 非同期セッションの作成
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# FastAPIの依存関係として利用するDBセッションジェネレータ
async def get_db():
    async with async_session as session:
        yield session