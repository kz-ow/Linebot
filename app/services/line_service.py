# app/services/line_service.py
from typing import List
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage,ImageSendMessage,
    FlexSendMessage, BubbleContainer, BoxComponent,
    TextComponent, ImageComponent, ButtonComponent, URIAction,
    CarouselContainer, SeparatorComponent
)
from app.config import settings
import time
from jose import jwk, jwt
from jose.utils import base64url_decode
from fastapi import Header, HTTPException, status
import httpx
import time

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
async def push_summarized_text(line_id: str, articles: str, summaries: str, images: List[str]):
    print("images[0]:", images[0])

    bubbles = [build_flex_for_article(a, s, i) for a, s, i in zip(articles, summaries, images)]
    print("bubbles[0]:", bubbles[0])
    carousel = CarouselContainer(contents=bubbles)
    flex = FlexSendMessage(
        alt_text='要約記事',
        contents=carousel
    )
    _push(line_id, flex)

# =================================================
# 4. IDトークン検証
# =================================================
LINE_VERYFY_URL = "https://api.line.me/oauth2/v2.1/verify"

async def verify_id_token(id_token: str) -> dict:
    """
    POST https://api.line.me/oauth2/v2.1/verify
    Content-Type application/x-www-form-urlencoded
    id_token=<IDトークン>
    client_id=<LINE_CHANNEL_ID>
    """

    header = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    params = {
        "id_token": id_token,
        "client_id": 2007363432,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LINE_VERYFY_URL,
            headers=header,
            params=params
        )
        response.raise_for_status()
        return response.json()

async def get_line_user_id(
    authorization: str | None = Header(None)
) -> str:
    """
    FastAPI の Depends に使う例。
    Authorization: Bearer <IDトークン> から、検証済みの sub（ユーザーID）を返す。
    """
    print("")
    print("[DEBUG] id_token:", authorization)
    print("")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing authorization header")
    id_token = authorization.split(" ", 1)[1]

    claims = await verify_id_token(id_token)
    return claims["sub"]


# =================================================
# 5. Flex Messageの作成
# =================================================
def build_flex_for_article(
    art: dict,
    summary: str,
    img_url: str | None = None
) -> BubbleContainer:
    # hero 部分（画像がなければ hero 自体を None にしてもOK）
    hero = ImageComponent(
        url=img_url,
        size="full",
        aspect_ratio="16:9",
        aspect_mode="cover"
    ) if img_url else None

    # ボディの中身
    body_contents = []
    if hero:
        body_contents.append(hero)

    body_contents.append(
        BoxComponent(
            layout="vertical",
            spacing="md",
            padding_all="16px",
            contents=[
                # タイトル
                TextComponent(
                    text=art.get("title", ""),
                    weight="bold",
                    size="xl",
                    wrap=True
                ),
                # 日付のみ（時計アイコン＋日付）
                TextComponent(
                    text=f"🕒 {art.get('published_date','')}",
                    size="xs",
                    color="#888888",
                    margin="sm"
                ),
                # 区切り線
                SeparatorComponent(margin="md"),
                # 要約
                TextComponent(
                    text=summary,
                    size="sm",
                    wrap=True,
                    margin="md"
                ),
            ]
        )
    )

    # フッター
    footer = BoxComponent(
        layout="vertical",
        spacing="sm",
        padding_all="16px",
        contents=[
            ButtonComponent(
                style="primary",
                height="sm",
                action=URIAction(
                    label="▶️ 詳細を見る",
                    uri=art.get("url", "")
                )
            )
        ]
    )

    return BubbleContainer(
        direction="ltr",
        body=BoxComponent(layout="vertical", contents=body_contents),
        footer=footer
    )

