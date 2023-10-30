import requests
import json

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

def write_message_sdata(data: dict):
    switch_data = {
        'text': data['events'][0]['message']['text'],
        'userId': data['events'][0]['source']['userId'],
        'groupId': data['events'][0]['source'].get('groupId', None),
        'timestamp': data['events'][0]['timestamp']
    }
    with open('switcher.json', 'r') as file:
        switcher = json.load(file)
    switcher['message'] = switch_data
    with open('switcher.json', 'w') as file:
        json.dump(switcher, file, indent=4, ensure_ascii=False)

def write_join_sdata(data: dict):
    switch_data = {
        'groupId': data['events'][0]['source']['groupId'],
        'timestamp': data['events'][0]['timestamp']
    }
    with open('switcher.json', 'r') as file:
        switcher = json.load(file)
    switcher['join'] = switch_data
    with open('switcher.json', 'w') as file:
        json.dump(switcher, file, indent=4)

def get_group_summary(group_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/group/{group_id}/summary'
    r = requests.get(url, headers=headers).json()
    return r

def get_user_profile(user_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    r = requests.get(url, headers=headers).json()
    return r
