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
app.mount("/liff", StaticFiles(directory="app/static/liff/"), name="liff")

app.include_router(line.router, prefix="/webhook", tags=["LineWebhook"])
app.include_router(news.router,   prefix="/news",    tags=["News"])
app.include_router(user.router,   prefix="/users",   tags=["User"])
app.include_router(register.router, prefix="/register",  tags=["Register"])

# health check endpoint
@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    健康チェック用のエンドポイント。
    アプリケーションが正常に動作しているかを確認します。
    """
    return {"status": "ok", "message": "Application is running smoothly."}

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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app.main_dev:app", host="0.0.0.0", port=80, reload=True)
