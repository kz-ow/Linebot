# app/main.py
from fastapi import FastAPI
from app.routers import line, news, user
from app.scheduler import start_scheduler

app = FastAPI(
    title="パーソナライズドニュースLINE Bot",
    description="ユーザーの興味に合わせたニュース要約をLINEで自動送信するアプリケーションです。",
    version="0.1.0"
)

app.include_router(line.router, prefix="/webhook", tag=["LineWebhook"])

app.include_router(news.router, prefix="/news", tags=["News"])

app.include_router(user.router, prefix="/users", tags=["User"])

@app.on_event("startup")
async def startup_event():
    start_scheduler()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)