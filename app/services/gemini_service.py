from google import genai
from app.config import settings
from google.genai import types
import asyncio
from typing import List

# APIキー＋リージョン指定でインスタンス化
client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    vertexai=False
)

# =================================================
# 記事ごと要約用テンプレート
# =================================================
SUMMARY_TEMPLATE = """
あなたはプロのニュース要約ツールです。以下のフォーマット以外の表現は一切不要です。

【タイトル】
{title}

【要約】
{body}
"""

async def summarize_one_article(title: str, body: str, max_tokens: int = 200) -> str:
    """
    1記事分の要約を Gemini に問い合わせて返す
    """
    prompt = SUMMARY_TEMPLATE.format(title=title, body=body)
    cfg = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=0.0,
    )
    resp = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=cfg,
    )
    return resp.text.strip()


async def summarize_articles(articles: List[dict]) -> List[str]:
    """
    複数記事を並列で要約
    """
    tasks = []
    print("[DEBAG] Gemini raw response[0]: ", articles)
    for art in articles:
        # 説明文が空なら本文(raw_content)を使う
        body = art.get("content") or art.get("description", "")
        tasks.append(summarize_one_article(art["title"], body))
    return await asyncio.gather(*tasks)
