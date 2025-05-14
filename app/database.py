# app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models.base import Base

# 非同期エンジンの作成
engine = create_async_engine(settings.POSTGRES_URL, echo=True)

# 非同期セッションの作成
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# FastAPIの依存関係として利用するDBセッションジェネレータ
async def init_models():
    import app.models.user
    import app.models.topic
    import app.models.user_topic
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise