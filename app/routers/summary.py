# # app/routers/summary.py
# from fastapi import APIRouter, HTTPException, Depends
# from app.services.summarization_service import summarize_text
# from app.database import get_db
# from sqlalchemy.orm import Session

# router = APIRouter()

# @router.get("/summary")
# async def get_summary(
#     db: Session = Depends(get_db),
#     category: str | None = None,
#     prompt: str | None = None
# ):
#     """
#     ニュース記事の要約を取得するエンドポイント。
#     :param db: データベースセッション
#     :param category: カテゴリフィルタ（オプション）
#     :param prompt: 要約のプロンプト（オプション）
#     :return: 要約されたニュース記事
#     """
#     try:
#         # ここで要約処理を行う
#         summary = await summarize_text(prompt) if prompt else None
#         return {"summary": summary}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))