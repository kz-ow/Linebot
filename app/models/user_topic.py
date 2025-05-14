from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class UserTopic(Base):
    __tablename__ = "user_topics"

    line_id    = Column(String, ForeignKey("users.line_id"), primary_key=True)
    topic_key  = Column(String, ForeignKey("topics.key"), primary_key=True)
    enabled    = Column(Boolean, default=True, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relations
    user  = relationship("User",  back_populates="topics")
    topic = relationship("Topic", back_populates="users")
