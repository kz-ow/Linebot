# api/routers/line.py
from fastapi import APIRouter, Request
from app.controllers import line_controller

router = APIRouter()

@router.post("/")
async def webhook(request: Request):
    """
    LINEプラットフォームからのWebhookを受け取るエンドポイント。
    Requestごと丸投げして、コントローラ内でbody, headersを参照します。
    """
    return await line_controller.handle_webhook(request)
