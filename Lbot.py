import flask
import json
import discord
from io import BytesIO
from apnggif import apnggif
from discord import SyncWebhook
from linebot import LineBotApi
from linebot.models import TextMessage

from utils.Ltools import get_user_profile, get_message_file, get_sticker_file, get_sticker_metadata, get_user_profile_from_group

with open('config.json', 'r') as file:
    config = json.load(file)
FILE_TYPE_TABLE = {
    'image': 'png',
    'video': 'mp4',
    'audio': 'mp3'
}
LANGUEGE_LIST = [
    'zh_TW',
    'ja',
    'ko',
    'en',
    'zh_CN'
]
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']
SECRET = config['LineBot']['CHANNEL_SECRET']
line_bot_api = LineBotApi(ACCESS_TOKEN)

app = flask.Flask(__name__)

@app.route("/", methods=['POST'])
def callback():
    with open('data.json', 'r') as file:
        data = json.load(file)
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    event = json.loads(body)['events'][0]
    print(event)

    if event['type'] == 'message':
        is_from_group =  event['source']['type'] == 'group'
        line_channel_id = event['source']['groupId'] if is_from_group else event['source']['userId']
        if line_channel_id not in data[f'{"group" if is_from_group else "user"}_table'].keys():
            webhook = SyncWebhook.from_url(data['logs_channel']['webhook'])
            webhook.send(f'New {"group" if is_from_group else "user"}: {line_channel_id}', username='Logs', silent=True)
        discord_channel_id = str(data[f'{"group" if is_from_group else "user"}_table'].get(line_channel_id, 0))
        if discord_channel_id in data['webhook_table'].keys():
            if is_from_group: user_profile = get_user_profile_from_group(event['source']['groupId'], event['source']['userId'])
            else: user_profile = get_user_profile(event['source']['userId'])
            webhook = SyncWebhook.from_url(data['webhook_table'][discord_channel_id])

            message_type = event['message']['type']

            if message_type == 'text':
                if event['message']['text'] == '-info':
                    with open('info.txt', 'r', encoding='utf8') as file:
                        info = file.read()
                    line_bot_api.reply_message(event['replyToken'], TextMessage(text=info))
                    return 'OK'
                webhook.send(event['message']['text'], username=user_profile['displayName'], avatar_url=user_profile.get('pictureUrl'))

            if message_type in ['image', 'video', 'audio', 'file']:
                with BytesIO() as file:
                    file.write(get_message_file(event['message']['id']))
                    file.seek(0)
                    if message_type == 'file': filename = event['message']['fileName']
                    else: filename = f'{message_type}.{FILE_TYPE_TABLE[message_type]}'
                    webhook.send(file=discord.File(file, filename=filename), username=user_profile['displayName'], avatar_url=user_profile.get('pictureUrl'))

            if message_type == 'sticker':
                is_apng = event['message']['stickerResourceType'] == 'ANIMATION'
                sticker = get_sticker_file(event['message']['stickerId'], event['message']['stickerResourceType'])

                sticker_series_metadata = get_sticker_metadata(event['message']['packageId'])
                for lang in LANGUEGE_LIST:
                    if lang in sticker_series_metadata['title'].keys():
                        series_name = sticker_series_metadata['title'][lang]
                        break
                for lang in LANGUEGE_LIST:
                    if lang in sticker_series_metadata['author'].keys():
                        author = sticker_series_metadata['author'][lang]
                        break
                sticker_description = f'{series_name}@{author}'
                sticker_name = sticker_series_metadata['title']['en'] + '-' + sticker_series_metadata['author']['en']

                with open('temp/sticker.png', 'wb') as file:
                    file.write(sticker)
                if is_apng:
                    apnggif('temp/sticker.png')
                    extension = 'gif'
                else: extension = 'png'

                webhook.send(content=f'**Sticker**-*{sticker_description}*', file=discord.File(f'temp/sticker.{extension}', filename=f'{sticker_name}.{extension}'), username=user_profile['displayName'], avatar_url=user_profile.get('pictureUrl'))

        return 'OK'

if __name__ == "__main__":
    if config['LineBot']['certification']:
        import ssl
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(config['LineBot']['certification']['cert'], config['LineBot']['certification']['key'])
        app.run(host=config['LineBot']['host'], port=config['LineBot']['port'], ssl_context=ssl_context)
    else:
        app.run(host=config['LineBot']['host'], port=config['LineBot']['port'])