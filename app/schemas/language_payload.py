# app.schemas.category_payload.py
from pydantic import BaseModel, Field, validator
from app.config import settings  # enum または定数集合


class LanguagePayload(BaseModel):
    lang : str = Field(
        default="日本語",
        description="Language code for the news articles. Default is '日本語'.",
    )

    @validator("lang")
    def check_topic(language: str) -> str:
        Language_Choices = settings.LANGUAGES
        if language not in Language_Choices:
            raise ValueError(f"invalid language: {language}")
        return language