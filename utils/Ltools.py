import requests
import json

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

def get_group_summary(group_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/group/{group_id}/summary'
    r = requests.get(url, headers=headers).json()
    return r

def get_user_profile(user_id: str) -> dict:
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    r = requests.get(url, headers=headers).json()
    return r
