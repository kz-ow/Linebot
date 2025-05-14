# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    line_id: str

class UserCreate(UserBase):
    interests: Optional[str] = None

class UserOut(UserBase):
    id: int
    is_subscribed: bool
    interests: Optional[str] = None

    class Config:
        orm_mode = True
