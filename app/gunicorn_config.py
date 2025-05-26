# /app/gunicorn_config.py
import asyncio
import multiprocessing
from apscheduler.schedulers.background import BackgroundScheduler

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"

preload_app = True

def on_starting(server):
    # モデルの初期化を非同期で実行
    server.log.info("Initializing master database...")
    asyncio.run(init_master_db())


def when_ready(server):
    # LIFFのHTMLファイルのビルドを非同期で実行
    server.log.info("Building LIFF HTML...")
    from app.build_html import build_liff_html
    build_liff_html()


# マスタープロセスで実行される初期化関数
async def init_master_db():
    from app.database import init_models
    await init_models()

