# app/services/news_service.py
import httpx
import feedparser
from app.config import settings

async def fetch_news_api(contry: str = "jp", category: str="general", pageSize: int = 5):
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "country": contry,
        "category": category,
        "pageSize": pageSize
    }

    async with httpx.AsyncClient() as client:
        response = client.get(settings.NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("articles", [])
    

async def fetch_ny_times_news(section: str = "home", limit: int = 5):
    params = {
        "api-key": settings.NewYorkTimes_API_KEY
    }
    async with httpx.AsyncClient as client:
        response = client.get(settings.NewYorkTimes_API_URL, params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("results", [])[:limit]
        mapped = []

        for article in articles:
            mapped.append({
                "source": "NYTimes",
                "title": article.get("title"),
                "description": article.get("abstract"),
                "url": article.get("url")
            })
    return mapped


async def get_combined_news(filtered_categories: str | None = None):
    news_api_articles = await fetch_news_api()
    line_news_articles = await fetch_ny_times_news()
    combined = []

    for article in news_api_articles:
        combined.append({
            "source": article.get("source", {}).get("name", "NewsAPI"),
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url")
        })
    combined.extend(line_news_articles)
    
    if filtered_categories:
    # 各記事が、登録されたどれかのカテゴリにマッチするかをチェック
        combined = [
            article for article in combined
            if any(
                fc.lower() in (article.get("title") or "").lower() or 
                fc.lower() in (article.get("description") or "").lower()
                for fc in filtered_categories
            )
        ]
    
    return combined
    