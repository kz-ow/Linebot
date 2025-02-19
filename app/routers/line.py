# app/routers/line.py
from fastapi import APIRouter, Request
from app.counrollers import line_countroler

router = APIRouter()

@router.post("/")
async def webhook(request: Request):
    raw_body = await request.body()
    headers = request.headers
    return await line_countroler.handle_webhook(raw_body, headers)