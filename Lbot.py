import flask
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextMessage, FileMessage, ImageMessage, StickerMessage, MessageEvent, VideoMessage, AudioMessage, JoinEvent
from linebot.exceptions import InvalidSignatureError

from utils.Ltools import write_message_sdata, write_file_sdata, write_image_sdata, write_sticker_sdata, write_video_audio_sdata, write_join_sdata

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']
SECRET = config['LineBot']['CHANNEL_SECRET']
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']

    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '-info':
        with open('info.txt', 'r', encoding='utf8') as file:
            info = file.read()
        line_bot_api.reply_message(event.reply_token, TextMessage(text=info))
        return
    write_message_sdata(event)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    write_sticker_sdata(event)

@handler.add(MessageEvent, message=FileMessage)
def handle_file(event):
    write_file_sdata(event)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    write_image_sdata(event)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    write_video_audio_sdata(event)

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    write_video_audio_sdata(event)

@handler.add(JoinEvent)
def handle_join(event):
    write_join_sdata(event)

    

if __name__ == "__main__":
    app.run(host=config['LineBot']['host'], port=config['LineBot']['port'])