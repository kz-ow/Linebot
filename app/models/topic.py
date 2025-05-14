# app/models/topic.py
from sqlalchemy import Column, String, event
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.config import settings

class Topic(Base):
    __tablename__ = "topics"

    # トピックのキー（例: "business", "sports"）
    key   = Column(String, primary_key=True, index=True)
    # 表示用ラベル（例: "ビジネス", "スポーツ"）
    label = Column(String, nullable=False)
    users = relationship(
        "UserTopic",
        back_populates="topic",
        cascade="all, delete-orphan",
    )

@event.listens_for(Topic.__table__, "after_create")
def seed_topics(target, connection, **kw):
    """
    PostgreSQL 用に ON CONFLICT DO NOTHING を付けて
    settings.TOPICS の key/label を一括投入します。
    """
    stmt = (
        insert(target)
        .values([{"key": k, "label": l} for k, l in settings.TOPICS])
        .on_conflict_do_nothing(index_elements=["key"])
    )
    connection.execute(stmt)