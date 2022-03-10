

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
import os

from ai import AI

from file import File

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
    
    message = TextSendMessage(text='讓我看看‘)
    line_bot_api.reply_message(event.reply_token, message)
    
    
    
@handler.add(MessageEvent, message=(ImageMessage))
def handel_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
        is_image = True
        
        
    if is_image = False:
        message_content = line_bot_api.get_message_content(event.message.id)
        img, file_path = file.save_bytes_image(message_content.content)
        pred = ai.predict_image_with_path(file_path)
        
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=pred)
                ])
#    if (event.message.type == "image"):
#        SendImage = line_bot_api.get_message_content(event.message.id)
#
#        local_save = './static/' + event.message.id + '.png'
#        with open(local_save, 'wb') as fd:
#            for chenk in SendImage.iter_content():
#                fd.write(chenk)
#
#        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = ngrok_url + "/static/" + event.message.id + ".png", preview_image_url = ngrok_url + "/static/" + event.message.id + ".png"))
        
        
ai = AI()
file = File()

if not os.path.exists('model/'):
    os.mekedirs('model/')
if not os.path.exists('media/'):
    os.mekedirs('media/')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
