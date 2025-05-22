# app/routers/user.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserOut
from app.crud.user import (
    get_or_create_user,
    set_subscription,
    get_subscription,
)
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    LINE ID を受け取ってユーザーを作成（または既存を返却）します。
    """
    return await get_or_create_user(db, user.line_id)


@router.put("/subscription", response_model=UserOut)
async def update_subscription(
    line_id: str,
    status: bool,
    db: AsyncSession = Depends(get_db),
):
    """
    購読ステータスを ON/OFF します。
    """
    user = await set_subscription(db, line_id, status)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/subscription", response_model=bool)
async def read_subscription(
    line_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    現在の購読ステータスを返します。
    """
    return await get_subscription(db, line_id)
