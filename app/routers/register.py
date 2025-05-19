from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.crud.user import set_categories
from app.schemas.category_payload import CategoryPayload
from app.services.line_service import get_line_user_id

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

from fastapi import Request
@router.post("/category/")
async def post_category(
    request: Request,
    payload: CategoryPayload,                     
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):      
    raw = await request.body()
    print("🔍 Raw request body:", raw.decode("utf-8"))
    # JSON デコード版も
    try:
        j = await request.json()
        print("🔍 Parsed JSON:", j)
    except Exception:
        print("⚠️ JSON parsing failed")
    await set_categories(db, user_id, payload.topic)



@router.post("/detail")
async def post_detail(
    payload: CategoryPayload,
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await set_categories(db, user_id, payload.topics)

@router.post("/regular")
async def post_regular(

):
    pass

@router.post("/")
async def test():
    return {"message": "Hello, World!"}