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
あなたはプロのニュース要約ツールです。以下のフォーマットで{language}要約しなでください。

【タイトル】
{title}

【要約】
{body}
"""


# 要点抽出テンプレート
_POINTS_TPL = """
以下の要約文から、重要な「要点」を３つまで、日本語の箇条書きで出力してください。
出力は「・」で始まるリストのみとしてください。

{summary}
"""

async def summarize_one_article(title: str, body: str, max_tokens: int = 200) -> str:
    """
    1記事分の要約を Gemini に問い合わせて返す
    """
    prompt = SUMMARY_TEMPLATE.format(title=title, body=body, language="日本語")
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
    for art in articles[:3]:
        # 説明文が空なら本文(raw_content)を使う
        body = art.get("content") or art.get("description", "")
        tasks.append(summarize_one_article(art["title"], body))
    return await asyncio.gather(*tasks)
