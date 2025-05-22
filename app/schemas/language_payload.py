# app.schemas.category_payload.py
from pydantic import BaseModel, Field, validator
from app.config import settings  # enum または定数集合


class LanguagePayload(BaseModel):
    language : str = Field(
        default="日本語",
        description="Language code for the news articles. Default is '日本語'.",
    )

    @validator("language")
    def check_topic(language: str) -> str:
        Language_Choices = [key for key, _ in settings.LANGUAGES]
        if language not in Language_Choices:
            raise ValueError(f"invalid language: {language}")
        return language