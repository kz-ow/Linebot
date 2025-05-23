from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.config import settings

async def get_or_create_user(db: AsyncSession, line_id: str) -> User:
    q = await db.execute(select(User).where(User.line_id == line_id))
    user = q.scalars().first()
    if not user:
        user = User(
            line_id=line_id, 
            is_subscribed=True, 
            scheduler=False, 
            endpoint_url=None,
            language="日本語", 
            mode="news")
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

async def set_subscription(db: AsyncSession, line_id: str, on: bool) -> User:
    user = await get_or_create_user(db, line_id)
    user.is_subscribed = on
    await db.commit()
    return user

async def get_subscription(db: AsyncSession, line_id: str) -> bool:
    q = await db.execute(select(User).where(User.line_id == line_id))
    user = q.scalars().first()
    return bool(user and user.is_subscribed)


async def set_language(
    db: AsyncSession,
    line_id: str,
    language: str,
):
    user = await get_or_create_user(db, line_id)
    user.language = language if language else "日本語"
    await db.commit()


async def set_scheduler(
    db: AsyncSession,
    line_id: str,
    scheduler: bool,
    endpointUrl: str
):
    user = await get_or_create_user(db, line_id)
    user.scheduler = scheduler
    user.endpoint_url = endpointUrl if scheduler else None
    await db.commit()

async def set_mode(
    db: AsyncSession,
    line_id: str,
    mode: str,
):
    user = await get_or_create_user(db, line_id)
    user.mode = mode
    await db.commit()

