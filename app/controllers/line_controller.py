import hmac, hashlib, base64, json
from typing import Dict, Any
from fastapi import HTTPException, Request
from app.config import settings
from app.database import async_session
from app.crud.user import (
    set_subscription,
    get_subscription,
    get_enabled_category,
)
from app.services.tavliy_services import search_articles
from app.services.line_service import (
    reply_text_message,
    push_summarized_text,
    push_text_message,
)
from app.services.gemini_service import summarize_articles

# ──────────────────────────────────────────────
#   署名検証
# ──────────────────────────────────────────────
def verify_signature(raw: bytes, sig: str) -> bool:
    digest = hmac.new(
        settings.LINE_CHANNEL_SECRET.encode(), raw, hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode() == sig

# ──────────────────────────────────────────────
#   Webhook エントリ
# ──────────────────────────────────────────────
async def handle_webhook(request: Request):
    raw = await request.body()
    sig = request.headers.get("X-Line-Signature", "")
    if not sig or not verify_signature(raw, sig):
        raise HTTPException(400, "Invalid signature")

    try:
        payload: Dict[str, Any] = json.loads(raw.decode())
    except json.JSONDecodeError:
        raise HTTPException(400, "Invalid JSON")

    events = payload.get("events", [])
    if not events:
        return {"status": "OK"}

    print(f"[INFO] payload: {payload}")

    async with async_session() as db:
        for event in events:
            ev_type = event.get("type")
            src     = event.get("source", {}) or {}
            line_id = src.get("userId")
            token   = event.get("replyToken")

            # ──────────── follow ────────────
            if ev_type == "follow" and line_id:
                await set_subscription(db, line_id, True)
                await push_text_message(
                    line_id,
                    "🎉 友だち追加ありがとうございます！\n"
                    "まずはリッチメニューの『トピック設定』から興味のある分野を選んでください。"
                )
                continue

            # ──────────── unfollow ───────────
            if ev_type == "unfollow" and line_id:
                await set_subscription(db, line_id, False)
                continue

            # ──────────── postback ───────────
            if ev_type == "postback" and line_id:
                data   = event["postback"].get("data", "")
                params = dict(p.split("=", 1) for p in data.split("&") if "=" in p)
                act    = params.get("action")

                if act == "subscribe":
                    await set_subscription(db, line_id, True)
                    if token:
                        await reply_text_message(token, "購読を開始しました！")
                    continue

                if act == "unsubscribe":
                    await set_subscription(db, line_id, False)
                    if token:
                        await reply_text_message(token, "購読を解除しました。")
                    continue

                if act == "status" and token:
                    sub = await get_subscription(db, line_id)
                    msg = "🎉 現在購読中です。" if sub else "🚫 未購読です。"
                    await reply_text_message(token, msg)
                    continue

                # 不明ポストバック
                if token:
                    await reply_text_message(token, "不明な操作です。メニューからお選びください。")
                continue

            # ──────────── message (text) ─────
            if (
                ev_type == "message"
                and event["message"].get("type") == "text"
                and line_id and token
            ):
                text = event["message"]["text"].strip()

                # 選択済みトピック取得（LIFF 側で保存されたもの）
                categories = await get_enabled_category(db, line_id)
                print(f"[INFO] User {line_id} category: {categories}")
                if not categories:
                    await reply_text_message(
                        token,
                        "トピックが設定されていません。\n"
                        "リッチメニューから『トピック設定』を開いてください。"
                    )
                    continue

                # 記事の検索
                articles, images = await search_articles(text=text)

                # 要約の取得
                summaries = await summarize_articles(articles=articles)

                await push_summarized_text(line_id=line_id, articles=articles, summaries=summaries, images=images)

                # 簡易 subscribe/unsubscribe/status コマンドも保持
                low = text.lower()
                if low in ("subscribe", "unsubscribe", "status"):
                    if low == "subscribe":
                        await set_subscription(db, line_id, True)
                        await reply_text_message(token, "購読を開始しました！")
                    elif low == "unsubscribe":
                        await set_subscription(db, line_id, False)
                        await reply_text_message(token, "購読を解除しました。")
                    else:
                        sub = await get_subscription(db, line_id)
                        msg = "🎉 現在購読中です。" if sub else "🚫 未購読です。"
                        await reply_text_message(token, msg)
                    continue

    return {"status": "OK"}
