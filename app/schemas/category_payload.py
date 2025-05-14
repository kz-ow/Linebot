# app.schemas.category_payload.py
from typing import List
from pydantic import BaseModel, Field, validator
from app.models.topic import TOPIC_CHOICES  # enum または定数集合


class CategoryPayload(BaseModel):
    topics: List[str] = Field(..., min_items=0)

    @validator("topics", each_item=True)
    def check_topic(cls, v: str) -> str:
        if v not in TOPIC_CHOICES:
            raise ValueError(f"invalid topic: {v}")
        return v