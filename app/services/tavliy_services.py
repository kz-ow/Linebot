from tavily import AsyncTavilyClient
from app.config import settings

# 環境変数などから読み込むのが安全です
client =  AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)

async def search_articles(
  text:str,
  mode: str = "news",
):
    if not text and text == "":
        raise ValueError("text must be provided")
    
    if mode == "news":
      response = await client.search(
          query=text,
          topic="news",
          days=4,
          limit=1,
          include_images = True,
      )

    elif mode == "general":
       response = await client.search(
          query=text,
          topic="general",
          days=4,
          limit=1,
          include_images = True,
      )
       
    return response.get("results", []), response.get("images", [])