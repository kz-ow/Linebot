import json
from linebot.models import FlexSendMessage
from app.config import settings
from app.database import async_session
from app.crud.user import get_enabled_category
from .line_service import line_bot_api

# ---------- Flex テンプレート（前回提示の完全版） ----------
BASE_FLEX: dict = {
    "type": "bubble",
    "size": "mega",
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
            {"type": "text", "text": "マイトピック設定", "size": "lg", "weight": "bold"},
            {"type": "separator"},
            {"type": "box", "layout": "vertical", "margin": "md", "contents": []},
            {
                "type": "button",
                "style": "primary",
                "margin": "lg",
                "height": "sm",
                "action": {
                    "type": "postback",
                    "label": "設定完了",
                    "data": "action=done",
                    "displayText": "設定を完了します"
                }
            }
        ]
    }
}

# ---------- row generator ----------
def _topic_row(code: str, jp: str, enabled: bool) -> dict:
    return {
        "type": "box",
        "layout": "horizontal",
        "contents": [
            {"type": "text", "text": jp, "flex": 3},
            {
                "type": "button",
                "flex": 2,
                "color": "#06C755" if enabled else "#BBBBBB",
                "action": {
                    "type": "postback",
                    "label": "● 選択中" if enabled else "○ 選択",
                    "data": f"action=select&topic={code}",
                    "displayText": f"{jp} を選択"
                }
            }
        ]
    }

# ---------- push flex ----------
async def send_topic_toggle_flex(line_id: str):

    print(f"send_topic_toggle_flex: {line_id}")

    async with async_session() as db:
        flags = await get_enabled_category(db, line_id)

    rows = [
        _topic_row(code, jp, flags.get(code, False))
        for code, jp in settings.TOPICS
    ]

    bubble = json.loads(json.dumps(BASE_FLEX))  # deep copy
    bubble["body"]["contents"][2]["contents"] = rows

    flex = FlexSendMessage(alt_text="トピック設定", contents=bubble)
    line_bot_api.push_message(line_id, flex)
