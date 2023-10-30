import flask
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

from utils.Ltools import write_message_sdata, write_join_sdata

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']
SECRET = config['LineBot']['CHANNEL_SECRET']

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def line_bot():
    data = json.loads(flask.request.get_data(as_text=True))
    print(data)

    _type = data['events'][0]['type']
    if _type=='message':
        if data['events'][0]['message']['type']=='text':
            write_message_sdata(data)
    elif _type=='join':
        write_join_sdata(data)

    return 'OK'

if __name__ == "__main__":
    app.run(host=config['LineBot']['host'], port=config['LineBot']['port'])