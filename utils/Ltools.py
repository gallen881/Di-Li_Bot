import requests
import json

from linebot.models.events import MessageEvent, JoinEvent

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

def write_message_sdata(event: MessageEvent):
    switch_data = {
        'text': event.message.text,
        'userId': event.source.user_id,
        'groupId': event.source.group_id if event.source.type == 'group' else None,
        'timestamp': event.timestamp
    }
    with open('switcher.json', 'r', encoding='utf8') as file:
        switcher = json.load(file)
    switcher['message'] = switch_data
    with open('switcher.json', 'w', encoding='utf8') as file:
        json.dump(switcher, file, indent=4, ensure_ascii=False)

def write_join_sdata(event: JoinEvent):
    switch_data = {
        'groupId': event.source.group_id,
        'timestamp': event.timestamp
    }
    with open('switcher.json', 'r', encoding='utf8') as file:
        switcher = json.load(file)
    switcher['join'] = switch_data
    with open('switcher.json', 'w', encoding='utf8') as file:
        json.dump(switcher, file, indent=4, ensure_ascii=False)

def write_file_sdata(event: MessageEvent):
    switch_data = {
        'message_id': event.message.id,
        'userId': event.source.user_id,
        'groupId': event.source.group_id if event.source.type == 'group' else None,
        'file_name': event.message.file_name,
        'file_size': event.message.file_size,
        'timestamp': event.timestamp
    }
    with open('switcher.json', 'r', encoding='utf8') as file:
        switcher = json.load(file)
    switcher['file'] = switch_data
    with open('switcher.json', 'w', encoding='utf8') as file:
        json.dump(switcher, file, indent=4, ensure_ascii=False)

def get_group_summary(group_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/group/{group_id}/summary'
    r = requests.get(url, headers=headers).json()
    return r

def get_user_profile(user_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    r = requests.get(url, headers=headers).json()
    return r

def get_message_file(message_id: str):
    url = f'https://api-data.line.me/v2/bot/message/{message_id}/content'
    r = requests.get(url, headers=headers)
    return r.content