import flask
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']
SECRET = config['LineBot']['CHANNEL_SECRET']

app = flask.Flask(__name__)

@app.route('/', methods=['POST'])
def line_bot():
    data = json.loads(flask.request.get_data(as_text=True))

    type = data['events'][0]['message']['type']
    print(data)
    if type=='text':
        switch_data = {
            'text': data['events'][0]['message']['text'],
            'userId': data['events'][0]['source']['userId'],
            'groupId': data['events'][0]['source'].get('groupId', None),
            'timestamp': data['events'][0]['timestamp']
        }
        with open('switcher.json', 'w') as file:
            json.dump(switch_data, file, indent=4)

    return 'OK'

if __name__ == "__main__":
    app.run(host=config['LineBot']['host'], port=config['LineBot']['port'])