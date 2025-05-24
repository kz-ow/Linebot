# app/scheduler.py
from sqlalchemy import func
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import async_session
from app.crud.user import get_all_users
from app.services.tavliy_services import serach_articles_for_scheduler
from app.services.gemini_service import summarize_articles_diffs
from app.services.line_service import push_summarized_text_scheduler, push_no_updated
from difflib import unified_diff
from datetime import datetime
import hashlib


# 日本（東京）向けタイムゾーンを指定したい場合
scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")

async def scheduled_personalized_news_summary():
    async with async_session() as session:
        # 1) DB から購読ユーザー一覧を取得
        users = await get_all_users(session)
        print(f"購読ユーザー数: {len(users)}")

        # 2) ユーザーごとに記事取得・要約・プッシュ送信
        for user in users:
            endpoint_url = user.endpoint_url

            print("[INFO] User:", user.line_id, "Endpoint URL:", endpoint_url)

            new_articles = []
            summaries   = []
            images      = []
            
            for wp in user.watched_pages:
                # --- ニュース取得 ---
                new_article = await serach_articles_for_scheduler(
                    endpoint_url=endpoint_url,
                )

                image = new_article[0]["images"]

                # --- 差分取得 & 要約 ---
                diff    = diff_articles(wp.last_content, new_article[0]["raw_content"])
                if not diff:
                    print(f"[INFO] No new content for {wp.url}")
                    diff = None
                    continue
                else:
                    summary = await summarize_articles_diffs(
                        articles_diffs=[diff],
                        language=user.language,
                    )

                # --- WatchedPage を直接更新 ---
                wp.last_content = new_article[0]["raw_content"]
                wp.last_checked = func.now()

                session.add(wp)

                await session.commit()
                await session.refresh(wp)


                new_articles.append(new_article)
                summaries.append(summary)
                images.append(image)
            
            
            if not new_articles:
                # 新着記事がない場合は「更新情報はありません」を送信
                await push_no_updated(user.line_id)
                continue
            else:
                # --- プッシュ送信 ---
                await push_summarized_text_scheduler(
                    line_id    = user.line_id,
                    articles   = new_articles,
                    summaries  = summaries,
                    images     = images,
                )


def diff_articles(old, new: str) -> str:
    """
    old: WatchedPage インスタンス（.last_content に前回テキスト）
    new: 今回取得したプレーンテキスト(raw_content)

    戻り値:
      raw_content と同様、改行込みの文字列として「新規に追加された行」だけを返す
    """
    # 古い・新しいテキストを行ごとに分割（改行を保持）
    old_text = old or ""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new.splitlines(keepends=True)

    diff_parts: list[str] = []
    for line in unified_diff(old_lines, new_lines, lineterm=""):
        if line.startswith("+") and not line.startswith("+++"):
            diff_parts.append(line[1:])

    # リストを連結して一つの文字列に
    return "".join(diff_parts)


def start_scheduler():
    # 毎朝 9:00 に定期実行
    scheduler.add_job(
        scheduled_personalized_news_summary,
        'cron',
        hour=23, minute=39)
    scheduler.start()
