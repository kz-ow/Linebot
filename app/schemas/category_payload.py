# app.schemas.category_payload.py
from typing import List
from pydantic import BaseModel, Field, validator
from app.config import settings  # enum または定数集合


class CategoryPayload(BaseModel):
    topics: List[str] = Field(..., min_items=0)

    @validator("topics", each_item=True)
    def check_topic(cls, v: str) -> str:
        TOPIC_CHOICES = [key for key, _ in settings.TOPICS]
        if v not in TOPIC_CHOICES:
            raise ValueError(f"invalid topic: {v}")
        return v