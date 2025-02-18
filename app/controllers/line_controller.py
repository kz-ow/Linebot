# api/controllers/line_controller.py
import hmac
import hashlib
import base64
import json
from fastapi import HTTPExeption
from app.services import line_service
from app.config import settings
from app.database import async_session
from app import crud
from app.schemas import UserCreate

async def handle_webhook(raw_body: bytes, headers):
    signature = headers.get('x-line-signature')
    if not signature or not verify_signature(raw_body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    payload = json.loads(raw_body)
    events = payload.get("events", [])
    if not events:
        raise HTTPException(status=400, detail="No events in payload")
    
    for event in events:
        print("Recived event: ", event)
        if event.get("type") == "message" and event.get("message", {}).get("type") == "text":
            text = event["message"]["text"].strip().lower()
            user_id =event["source"]["userId"]

            if text == "subscribe":
                updated_user = await crud.update_user_subscription_status(db, user_id, True)
                if updated_user:
                    await line_service.send_text_message(user_id, "購読設定が有効になりました。")
                else:
                    new_user = await crud.create_user(db, UserCreate(line_id=user_id))
                    await line_service.send_text_message(user_id, "新規登録され，購読設定が有効になりました。")
            elif text == "unsubscribe":
                updated_user = await crud.update_user_subcription_status(db, user_id, False)
                if updated_user:
                    await line_service.send_text_message(user_id, "購読設定が無効になっています。")
                else:
                    await line_service.send_text_message(user_id, "購読設定が無効になっています。")
            else:
                await line_service.send_text_message(user_id, "コマンドが認識されません。 'subscribe' または 'unsubscribe' を送信してください。")
    return {"status": "OK"}


# 署名の検証（HMACを用いたHMAC-SHA256認証: LINE Botの標準の認証方法）
# 受信リクエストの認証: リクエストの真正性のみを検証
# 受信したリクエストのBodyのハッシュ値とリクエストヘッダのx-line-signatureの検証
def verify_signature(raw_body:bytes, signature: str) -> bool:
    hash_digest = hmac.new(
        settings.LINE_CHANNEL_SECRET.encode('utf-8'),
        raw_body,
        hashlib.sha256
    ).digest()

    computed_signature = base64.b64encode(hash_digest).decode('utf-8')
    return computed_signature == signature

                

