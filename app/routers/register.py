from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, Header, HTTPException, status, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import async_session
from app.crud.user import set_categories
from app.schemas.category_payload import CategoryPayload

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def get_line_user_id(
    authorization: Annotated[str | None, Header()] = None
) -> str:
    """
    Authorization: Bearer <LIFF ID Token> から userId を取得
    """
    print(f"[INFO] Authorization: {authorization}")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "missing id_token")

    id_token = authorization.split(" ", 1)[1]
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.line.me/oauth2/v2.1/verify",
            data={
                "id_token": id_token,
                "client_id": settings.LINE_CHANNEL_SECRET
            },
        )
    if resp.status_code != 200:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid id_token")

    return resp.json()["sub"]  # LINE userId


@router.post("/category")
async def post_category(
    payload: CategoryPayload,                     
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):  
    print(f"[INFO] Received category payload: {payload}")
    await set_categories(db, user_id, payload.topics)

@router.post("/detail")
async def post_detail(
    payload: CategoryPayload,
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    print(f"[INFO] Received detail payload: {payload}")
    await set_categories(db, user_id, payload.topics)

@router.post("/regular")
async def post_regular(

):
    pass

@router.post("/")
async def test():
    return {"message": "Hello, World!"}