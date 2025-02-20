from pydantic import Basemodel
from typing import Optional
from datetime import datetime

# NewsArticle用のスキーマ
class NewsArticleBase(Basemodel):
    title: str
    description: Optional[str] = None
    url = Optional[str] = None
    source: Optional[str] = None

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticleOut(NewsArticleBase):
    id: int
    published_at: datetime

    class Config:
        orm_mode = True

# ユーザー用のスキーマ
class UserBase(Basemodel):
    line_id: str

class UserCreate(UserBase):
    id: int #ユーザーID（データベース内での識別番号）
    is_subscribed: bool
    interests: Optional[str] = None

    class Config:
        orm_mode = True



