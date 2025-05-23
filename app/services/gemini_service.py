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
あなたはプロのニュース要約ツールです。以下のフォーマットで{language}で要約してください。
また，要約は200文字以内に収めてください。
【タイトル】
{title}

【要約】
{body}
"""

async def summarize_one_article(title: str, body: str, max_tokens: int = 300, language: str ="日本語") -> str:
    prompt = SUMMARY_TEMPLATE.format(title=title, body=body, language=language)
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


async def summarize_articles(articles: List[dict], language: str) -> List[str]:
    """
    複数記事を並列で要約
    """
    tasks = []
    for art in articles[:3]:
        # 説明文が空なら本文(raw_content)を使う
        body = art.get("content") or art.get("description", "")
        tasks.append(summarize_one_article(art["title"], body, language=language))
    return await asyncio.gather(*tasks)


async def summarize_articles_diffs(articles_diffs: List[dict], language: str) -> List[str]:
    """
    Tavily Extractで取得した記事の差分を要約
    """



    
