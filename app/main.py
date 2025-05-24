# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool
from app.routers import line, news, user, register
from app.database import init_models
from app.build_html import build_liff_html
from app.scheduler import start_scheduler
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="パーソナライズドニュースLINE Bot",
    description="ユーザーの興味に合わせたニュース要約をLINEで自動送信するアプリケーションです。",
    version="0.1.0",
    redirect_slashes=False
)

# LIFFのHTMLファイルを提供するためのルーティング
app.mount("/liff", StaticFiles(directory="app/static/liff/html/"), name="liff")

app.include_router(line.router, prefix="/webhook", tags=["LineWebhook"])
app.include_router(news.router,   prefix="/news",    tags=["News"])
app.include_router(user.router,   prefix="/users",   tags=["User"])
app.include_router(register.router, prefix="/register",  tags=["Register"])

@app.on_event("startup")
async def startup_event():
    try:
        import app.models.user
        
        await init_models()
        logger.info("データベースの初期化に成功しました。")
    except Exception as e:
        logger.exception(f"データベースの初期化に失敗しました: {e}")

    try:
        await run_in_threadpool(build_liff_html)
        logger.info("LIFFのHTMLファイルのビルドに成功しました。")
    except Exception as e:
        logger.exception(f"LIFFのHTMLファイルのビルドに失敗しました: {e}")

    try:
        start_scheduler()
        logger.info("スケジューラーの初期化に成功しました。")
    except Exception as e:
        logger.exception(f"スケジューラーの初期化に失敗しました: {e}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
