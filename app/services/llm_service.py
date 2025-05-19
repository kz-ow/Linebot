from google import genai
from app.config import settings
from google.genai import types

# APIキー＋リージョン指定でインスタンス化
client = genai.Client(
    api_key=settings.GEMINI_API_KEY,
    vertexai=False
)

# =================================================
# 要約テンプレート
# =================================================

SUMMARY_TEMPLATE = """
あなたはプロのニュース要約ツールです。以下のフォーマット以外の表現は一切不要です。

【タイトル】
（記事のタイトルをそのまま）

【要約】
（記事の本文や説明から、150字以内で事実のみを簡潔に要約）

【詳細URL】
（記事の URL）

【発信元】
（ニュースソース名）

【発信日時】
（ISO 8601 形式：YYYY-MM-DDThh:mm:ssZ）
"""


def build_news_prompt(articles: list[dict]) -> str:
    """
    articles: [
      {
        "title": str,
        "description": str,
        "url": str,
        "source": str,
        "published_at": str
      },
      ...
    ]
    を以下のようなテキストに変換します:
    
    タイトルA
    説明A
    URLA
    発信元A
    日時A

    タイトルB
    説明B
    URLB
    発信元B
    日時B

    ...
    """
    blocks = []
    for a in articles:
        blocks.append(
            "\n".join([
                a["title"],
                a.get("description", ""),
                a.get("url", ""),
                a.get("source", ""),
                a.get("published_at", "")
            ]).strip()
        )
    # 各記事ブロックを二重改行で区切る
    return "\n\n".join(blocks)

async def summarize(articles: list[dict], max_tokens: int = 2048) -> str:
    # 1) プロンプト用テキスト生成
    news_text = build_news_prompt(articles)
    prompt = SUMMARY_TEMPLATE + "\n" + news_text
    print(f"[DEBUG] Full prompt:\n{prompt}\n--- end prompt ---")

    # 2) 設定
    gen_cfg = types.GenerateContentConfig(
        max_output_tokens=max_tokens,
        temperature=0.2,
        # stop_sequences は外して最大トークン数で制御するか、
        # 明示的な区切りトークンを使ってください
        # stop_sequences=["\n1. "]  # 例えば次のリスト番号で止める
    )

    # 3) 実行
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=prompt,
        config=gen_cfg,
    )
    print(f"[DEBUG] Gemini raw response:\n{response}\n--- end response ---")

    return response.text
