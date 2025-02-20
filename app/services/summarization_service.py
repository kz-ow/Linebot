# app/services/summarization_service.py
import httpx
from app.config import settings

async def summarize_text(text: str) -> str:
    # ローカルに立ち上げたGammaのエンドポイントへリクエストを送信
    url = settings.Gemma_LOCAL_API_URL
    payload = {
        "prompt": f"以下のニュース記事を要約してください:\n\n{text}",
        "max_tokens": 150,
        "temperture": 0.5
    }

    async with httpx.AsyncClinet() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        summary = data.get("summary", "").strip()
        return summary

