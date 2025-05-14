# app/routers/news.py
from app.services.llm_service import summarize
from fastapi import APIRouter, HTTPException
from app.services import news_service

router = APIRouter()

@router.get("/combined")
async def get_combined_news(category: str | None = None):
    try:
        filtered_categories = [c.strip() for c in category.split(",")] if category else None
        articles = await news_service.get_combined_news(filtered_categories)
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def get_news_summary(prompt: str):
    try:
        summary = await summarize(prompt)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
