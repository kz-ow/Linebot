from tavily import AsyncTavilyClient
from app.config import settings

# 環境変数などから読み込むのが安全です
client =  AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)

async def search_articles(
  text:str,
):
    response = await client.search(
        query=text,
        topic="news",
        days=4,
        limit=1,
        include_images = True,

    )
    
    return response.get("results", []), response.get("images", [])