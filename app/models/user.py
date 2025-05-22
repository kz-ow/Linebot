# app/models/user.py
import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

# 中間テーブル定義はどちらか片側のファイルに置けばOKです
class User(Base):
    __tablename__ = "users"

    line_id       = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    is_subscribed = Column(Boolean, default=True)
    schedules = Column(Boolean, nullable=False, default=False)
    endpoint_url = Column(String, nullable=True, default=None)
    language = Column(String, nullable=False, default="日本語")
    mode = Column(String, nullable=False, default="general")