from flask import Flask, request, abort

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

from VersaLog import *
from dotenv import load_dotenv
from datetime import datetime
import os
import api_req


load_dotenv()

logger = VersaLog(enum="detailed", show_tag=True, tag="Request")

app = Flask(__name__)

configuration = Configuration(
    access_token=os.getenv("LINE_CHANNEL_TOKEN")
)
handler = WebhookHandler(
    os.getenv("LINE_CHANNEL_SECRET")
)

TARGET_GROUP_ID = os.getenv("GROUP_ID")
WEATHER_API_KEY = os.getenv("KEYS")

def log_and_push(level: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"[{level.upper()}] {timestamp}\n{message}"

    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warn":
        logger.warn(message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=TARGET_GROUP_ID,
                messages=[TextMessage(text=log_text)]
            )
        )


def run_weather_check():
    success, result = api_req.get_weather(
        location="Tokyo",
        api_key=WEATHER_API_KEY
    )

    if success:
        log_and_push("info", "天気APIの取得に成功しました")
    else:
        log_and_push("error", f"天気APIの取得に失敗しました: {result}")

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text.strip()

    if text == "log":
        run_weather_check()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
