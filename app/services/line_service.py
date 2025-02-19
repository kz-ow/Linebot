# app/services/line_service.py
import httpx
from app.config import settings

async def send_text_message(to: str, message: str):
    url = "https://api.line.me/v2/bot/message/push"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LINE_CHANNEL_ACCESS_TOKEN}",
    }

    data = {
        "to": to,
        "messages": [
            {"type": "text", "text": message}
        ]
    }
    
    # WEBクライアントを用いてメールを送信
    async with httpx.AsyncClinet() as client:
        response = await client.post(url, json=data, headers=headers)
        response.raise_for_status()
        print("Message sent successfully", response.json())
        return response.json()

