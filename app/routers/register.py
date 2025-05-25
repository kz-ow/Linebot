from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.crud.user import set_scheduler, set_language, set_mode
from app.schemas.scheduler_payload import SchedulerPayload
from app.schemas.mode_payload import ModePayload
from app.schemas.language_payload import LanguagePayload
from app.services.line_service import get_line_user_id

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

@router.post("/mode")
async def post_mode(
    payload: ModePayload,                     
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):  
    print(f"[INFO] post_mode: {payload.mode}")
    await set_mode(db, user_id, payload.mode)


@router.post("/language")
async def post_language(
    payload: LanguagePayload,
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    print(f"[INFO] post_lang: {payload.lang}")
    await set_language(db, user_id, payload.lang)

@router.post("/scheduler")
async def post_scheduler(
    payload: SchedulerPayload,
    user_id: Annotated[str, Depends(get_line_user_id)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    await set_scheduler(db, user_id, payload.scheduler, payload.endpointUrl)


# テスト用
# from fastapi import Request
# @router.post("/language")
# async def register_language(
#     request: Request,
#     user_id: Annotated[str, Depends(get_line_user_id)],
#     db: Annotated[AsyncSession, Depends(get_db)],
# ):
#     """
#     テスト用の言語登録エンドポイント
#     """
#     body = await request.json()
#     print(f"[INFO] raw request body: {body}")

