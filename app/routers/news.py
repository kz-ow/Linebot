# app/routers/news.py
from app.services.tavliy_services import search_articles
from app.services.gemini_service import summarize_articles
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/combined")
async def get_combined_news(text: str | None = None):
    try:
        articles = await search_articles(text)
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def get_news_summary(ariticles: str):
    try:
        summary = await summarize_articles(ariticles)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
