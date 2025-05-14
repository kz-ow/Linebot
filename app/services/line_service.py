# app/services/line_service.py
from __future__ import annotations
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
)
from app.config import settings
from app.services.llm_service import summarize

# ────────────────────────────────────────────────
# LINE SDK インスタンス
# ────────────────────────────────────────────────
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

# =================================================
# 汎用送信ユーティリティ（ラップ）
# =================================================
def _push(user_id: str, message):
    line_bot_api.push_message(user_id, message)

def _reply(reply_token: str, message):
    line_bot_api.reply_message(reply_token, message)

# =================================================
# 1. テキスト
# =================================================
async def reply_text_message(reply_token: str, text: str):
    _reply(reply_token, TextSendMessage(text=text))

async def push_text_message(user_id: str, text: str):
    _push(user_id, TextSendMessage(text=text))

# =================================================
# 2. 画像
# =================================================
async def reply_image_message(reply_token: str, image_url: str):
    _reply(reply_token, ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url))

async def push_image_message(user_id: str, image_url: str):
    _push(user_id, ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=image_url))

# =================================================
# 3. 要約
# =================================================
async def push_summarized_text(line_id: str, articles: str):
    print(f"articles: {articles}")
    summary = await summarize(articles)
    print(f"push_summarized_text: {summary}")
    _push(line_id, TextSendMessage(text=summary))


