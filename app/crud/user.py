from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.user import User
from app.models.watched_page import WatchedPage
from app.services.tavliy_services import serach_articles_for_scheduler
import hashlib
from datetime import datetime

async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.execute(
        select(User)
        .options(
            selectinload(User.watched_pages)  # ← ここで watched_pages を一括ロード
        )
    )
    return result.scalars().all()

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
            mode="general")
        
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

    if user.scheduler and user.endpoint_url:
        # 初回記事を取得
        article = await serach_articles_for_scheduler(
            endpoint_url=user.endpoint_url,
        )
        raw_content = article[0]["raw_content"]

        stmt = insert(WatchedPage).values(
            user_id=user.line_id,
            url=user.endpoint_url,
            last_content=raw_content,
            last_checked=func.now()
        ).on_conflict_do_update(
            index_elements=['user_id', 'url'],
            set_={
                'last_content': raw_content,
                'last_checked': func.now(),
            }
        )
        await db.execute(stmt)
    else: # schedulerが無効化された場合は、関連するWatchedPageを削除
        await db.execute(
            WatchedPage.__table__.delete().where(WatchedPage.user_id == user.line_id)
        )

    await db.commit()

async def set_mode(
    db: AsyncSession,
    line_id: str,
    mode: str,
):
    user = await get_or_create_user(db, line_id)
    user.mode = mode
    await db.commit()
    

