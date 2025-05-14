from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.topic import Topic
from app.models.user_topic import UserTopic
from app.config import settings

async def get_or_create_user(db: AsyncSession, line_id: str) -> User:
    q = await db.execute(select(User).where(User.line_id == line_id))
    user = q.scalars().first()
    if not user:
        user = User(line_id=line_id, is_subscribed=True)
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

async def set_single_category(
    db: AsyncSession,
    line_id: str,
    topic_key: str
) -> str:
    user: User = await get_or_create_user(db, line_id)

    # ① まず既存行を全部 False
    await db.execute(
        update(UserTopic)
        .where(UserTopic.line_id == user.line_id)
        .values(enabled=False)
    )

    # ② この topic_key を True で UPSERT
    stmt = pg_insert(UserTopic).values(
        line_id=user.line_id,
        topic_key=topic_key,
        enabled=True,
    ).on_conflict_do_update(
        index_elements=["line_id", "topic_key"],
        set_={"enabled": True}
    )
    await db.execute(stmt)
    await db.commit()
    return topic_key

async def get_enabled_category(
    db: AsyncSession,
    line_id: str
) -> list[str]:
    """
    enabled=True の topic_key 一覧を返す。
    OFF の行は含まれない。
    """
    rows = await db.execute(
        select(UserTopic.topic_key)
        .where(
            UserTopic.line_id == line_id,
            UserTopic.enabled.is_(True)
        )
    )
    enabled_keys = {r[0] for r in rows.all()}

    category_dict = {
        code: (code in enabled_keys)
        for code, _ in settings.TOPICS
    }

    return category_dict

async def set_categories(
    db: AsyncSession,
    line_id: str,
    topics: list[str],
) -> list[str]:
    """
    LIFF から送られてきた topic 配列で
    UserTopic テーブルを一括更新する。
    1) topics に含まれない行は enabled=False
    2) topics に含まれる行は INSERT or UPDATE(enabled=True)
    """
    # ユーザー行を保証
    user = await get_or_create_user(db, line_id)

    # ① topics に入っていない既存行を OFF
    if topics:
        await db.execute(
            update(UserTopic)
            .where(
                UserTopic.line_id == user.line_id,
                UserTopic.topic_key.not_in(topics)
            )
            .values(enabled=False)
        )
    else:
        # 何も選ばれていない場合は全 OFF
        await db.execute(
            update(UserTopic)
            .where(UserTopic.line_id == user.line_id)
            .values(enabled=False)
        )

    # ② topics に入っているものを UPSERT(enabled=True)
    if topics:
        stmt = (
            pg_insert(UserTopic)
            .values([
                {"line_id": user.line_id, "topic_key": t, "enabled": True}
                for t in topics
            ])
            .on_conflict_do_update(
                index_elements=["line_id", "topic_key"],
                set_={"enabled": True}
            )
        )
        await db.execute(stmt)

    await db.commit()
    return topics
