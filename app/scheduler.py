# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import async_session
from app.crud import get_all_users
from app.services import line_service, news_service, summarization_service

scheduler = AsyncIOScheduler()

async def scheduled_personalized_news_summary():
    async with async_session() as settion:
        users = await get_all_users(settion)
    
    for user in users:
        #　ユーザーの興味のあるカテゴリーを抽出
        interests = []
        if users.interests:
            interests = [interest.stripe() for interest in user.interests.split(",")]
        else:
            continue

        combined_news = await news_service.get_combined_news(filtered_category=interests)

        if not combined_news:
            print(f"ユーザー{user.line_id}：　該当するニュースが見つかりませんでした")
            continue
            
        news_text = "\n".join([f"{item['title']}: {item['description']}" for item in combined_news])
        try:
            summary = await summarization_service.summrize_text(news_text)
        except Exception as e:
            print(f"ユーザー{user.line_id}:　要約に失敗: {e}")
            summary = "要約に失敗しました"
        
        try:
            await line_service.send_text_message(user.line_id, summary)
            print(f"ユーザー{user.line_id}にパーソナライズされた要約を送信しました。")
        except Exception as e:
            print("ユーザー{user.line_id}への要約送信エラーが発生しました。")

def start_scheduler():
    scheduler.add_job(scheduled_personalized_news_summary, 'cron', hour=9, minute=0)
    scheduler.start()
    print("Scheduler started")



            

    

    

