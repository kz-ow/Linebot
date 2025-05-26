from tavily import AsyncTavilyClient
from app.config import settings

# 環境変数などから読み込むのが安全です
client =  AsyncTavilyClient(api_key=settings.TAVILY_API_KEY)

# LINE BOTからのリクエストを処理
async def search_articles(
  text:str,
  mode: str
):
    if not text and text == "":
        raise ValueError("text must be provided")
    
    response = await client.search(
        query=text,
        topic=mode,
        days=4,
        limit=1,
        include_images = True,
    )

    return response.get("results", []), response.get("images", [])

# 定期更新用(Extract)
async def serach_articles_for_scheduler(
    endpoint_url: str,
):
    if not endpoint_url and endpoint_url == "":
        raise ValueError("endpoint_url must be provided")

    response = await client.extract(
        urls=[endpoint_url],
        include_images=True
    )

    if not response:
        raise ValueError("response is empty")

    return response.get("results", [])