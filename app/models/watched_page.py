# app/models/watched_page.py
from sqlalchemy import (
    Column, BigInteger, Text, String,
    TIMESTAMP, ForeignKey, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.models.base import Base


class WatchedPage(Base):
    __tablename__ = "watched_pages"
    __table_args__ = (
        UniqueConstraint("user_id", "url", name="uq_user_url"),
    )

    id            = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id       = Column(
        String, 
        ForeignKey("users.line_id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    url           = Column(Text, nullable=False)
    last_hash     = Column(String, nullable=False, default="")     # 差分検知用ハッシュ
    last_content  = Column(Text,   nullable=False, default="")     # 前回取得テキスト
    last_checked  = Column(
        TIMESTAMP(timezone=True), 
        nullable=False, 
        server_default=func.now()
    )

    # User モデル側の watched_pages と相互リンク
    user = relationship("User", back_populates="watched_pages")
