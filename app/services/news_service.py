import httpx
from typing import List, Optional
from dateutil import parser
from app.config import settings
import deepl

translator = deepl.Translator(auth_key=settings.DEEPL_API_KEY)


async def fetch_latest_news_by_category(
    categories: Optional[str] = None,
    keywords: Optional[List[str]] = None,
    page_size: int = 5,
    country: str = "us",
) -> List[dict]:
    """
    - keywords に日本語が含まれていれば、英語に翻訳してから検索。
    - 翻訳したキーワード＋カテゴリをクエリに組み込みます。
    """
    # --- キーワードの正規化 ---
    # 例）["AI", "AI技術", "AI技術の進化"] → [AI AND AI技術 AND AI技術の進化]
    keyword_query = ""
    for i, keyword in enumerate(keywords):
        if i == 0:
            if keywords and categories:
                keyword_query += f"{keyword}"
                break
        elif i == len(keywords) - 1:
            keyword_query += f"{keyword}"
        else:
            keyword_query += f" {keyword}"
    
    translated_keywords = translator.translate_text(
        keyword_query,
        target_lang="EN-US",
        source_lang="JA",
    )
    
    selected_category = [category for category, enabled in categories.items() if enabled] if categories else []

    print(f"[INFO] selected_category: {selected_category}")
    print(f"[INFO] translated_keywords: {translated_keywords}")
    combined = []

    # --- NewsAPI リクエスト ---
    # 最新ニュースがほしい場合
    if selected_category and translated_keywords:
        news_url = "https://newsapi.org/v2/top-headlines"
        news_params = {
            "apiKey":   settings.NEWS_API_KEY,
            "category": selected_category[0],
            "pageSize": page_size,
            "q":        translated_keywords,
        }
    
    # より詳細な情報がほしい場合
    elif translated_keywords:
        news_url = "https://newsapi.org/v2/everything"
        news_params = {
            "apiKey":   settings.NEWS_API_KEY,
            "q":        translated_keywords,
            "sortBy":   "publishedAt",
            "pageSize": page_size,
        }

    # 定期更新の場合
    else:
        news_url = "https://newsapi.org/v2/top-headlines"
        news_params = {
            "apiKey":   settings.NEWS_API_KEY,
            "pageSize": page_size,
            "category": selected_category[0]
        }

    async with httpx.AsyncClient() as client:
        resp = await client.get(news_url, params=news_params)
        resp.raise_for_status()
        data = resp.json()

    for art in data.get("articles", [])[:page_size]:
        combined.append({
            "source":       art["source"]["name"],
            "title":        art["title"],
            "description":  art["description"],
            "url":          art["url"],
            "image_url":    art.get("urlToImage"),
            "published_at": art.get("publishedAt"),
        })

    print("[INFO] article fetched from NewAPI: ")
    print(combined)

    # --- 両方マージして最新順ソート ---
    combined.sort(key=lambda x: parser.isoparse(x["published_at"]), reverse=True)
    return combined
