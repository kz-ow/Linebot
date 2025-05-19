# # app/scheduler.py
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from app.database import async_session
# from app.crud.user import get_all_users
# from app.services.tavliy_services import 
# from app.services.gemini_service import summarize_articles
# from app.services.line_service import push_text_message

# # 日本（東京）向けタイムゾーンを指定したい場合
# scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")

# async def scheduled_personalized_news_summary():
#     # 1) DB から購読ユーザー一覧を取得
#     async with async_session() as session:
#         users = await get_all_users(session)

#     # 2) ユーザーごとに記事取得・要約・プッシュ送信
#     for user in users:
#         # --- 興味カテゴリのパース ---
#         if user.interests:
#             interests = [i.strip() for i in user.interests.split(",")]
#         else:
#             interests = []

#         # --- ニュース取得 ---
#         articles = await get_combined_news(interests)
#         if not articles:
#             print(f"ユーザー {user.line_id}: 該当するニュースが見つかりませんでした。")
#             continue

#         # --- 要約用テキスト整形（上位 5 件程度）---
#         snippets = []
#         for a in articles[:5]:
#             title = a.get("title", "")
#             desc  = a.get("description", "")
#             snippets.append(f"{title}\n{desc}")
#         news_text = "\n\n".join(snippets)

#         # --- 要約実行 ---
#         try:
#             summary = await summarize_articles(news_text)
#         except Exception as e:
#             print(f"ユーザー {user.line_id}: 要約失敗: {e}")
#             summary = "要約に失敗しました。"

#         # --- LINE へプッシュ ---
#         try:
#             await push_text_message(user.line_id, summary)
#             print(f"ユーザー {user.line_id} に要約を送信しました。")
#         except Exception as e:
#             print(f"ユーザー {user.line_id} への送信エラー: {e}")

# def start_scheduler():
#     # 毎朝 9:00 に定期実行
#     scheduler.add_job(
#         scheduled_personalized_news_summary,
#         'cron',
#         hour=9, minute=0
#     )
#     scheduler.start()
