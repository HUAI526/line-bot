from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('/70xzFRRZV5uxCKKMhxxBbbGaUjSIWz2CdeG8br9ukFT2XNgWjLEt8ZWZsAyPmkbHppAQK3xKfZC+UQAyaNXxiVzm77k590V0oanRB+nw6nHfXqqu0Sv6Ttt4EdFtBNNEk8z8AfRBx2fObeET9w8OQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a130514785636139f01b806ffa3d2366')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你好啊'))


if __name__ == "__main__":
    app.run()