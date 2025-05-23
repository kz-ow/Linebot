# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import async_session
from app.crud.user import get_all_users
from app.services.tavliy_services import serach_articles_for_scheduler
from app.services.gemini_service import summarize_articles
from app.services.line_service import push_summarized_text
from app.services

# 日本（東京）向けタイムゾーンを指定したい場合
scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")

async def scheduled_personalized_news_summary():
    # 1) DB から購読ユーザー一覧を取得
    async with async_session() as session:
        users = await get_all_users(session)
    print(f"購読ユーザー数: {len(users)}")

    # 2) ユーザーごとに記事取得・要約・プッシュ送信
    for user in users:
        # --- ユーザー情報の取得 ---
        endpoint_url = user.endpoint_url

        old_articles = user.watched_pages

        articles_diffs = []
        summaries = []

        for old_article in old_articles:
            # --- ニュース取得 ---
            new_article, images = await serach_articles_for_scheduler(
                endpoint_url=endpoint_url,
            )

            # 取得した記事の中から、前回の情報との差分を取得
            diff = diff_articles(old_article, new_article)

            # --- 要約 ---
            summaries = await summarize_articles(diff, language=user.language)

            # --- 差分を保存 ---

        # --- プッシュ送信 ---
        await push_summarized_text(line_id=user.line_id, articles=articles, summaries=summaries, images=images)

def diff_articles(old, new):
    diff = []
    return diff


def start_scheduler():
    # 毎朝 9:00 に定期実行
    scheduler.add_job(
        scheduled_personalized_news_summary,
        'cron',
        hour=15, minute=45)
    scheduler.start()
