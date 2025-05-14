# app/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base

# 中間テーブル定義はどちらか片側のファイルに置けばOKです


class User(Base):
    __tablename__ = "users"

    line_id       = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    is_subscribed = Column(Boolean, default=True)
    topic_flags = Column(JSONB, nullable=False, default=dict)
    topics = relationship(
        "UserTopic",
        back_populates="user",
        cascade="all, delete-orphan",
    )
