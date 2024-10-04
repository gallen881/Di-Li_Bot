import requests
import json

from linebot.models.events import MessageEvent, JoinEvent

with open('config.json', 'r') as file:
    config = json.load(file)
ACCESS_TOKEN = config['LineBot']['ACCESS_TOKEN']

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

def get_group_summary(group_id) -> dict:
    url = f'https://api.line.me/v2/bot/group/{group_id}/summary'
    r = requests.get(url, headers=headers).json()
    return r

def get_user_profile(user_id) -> dict:
    url = f'https://api.line.me/v2/bot/profile/{user_id}'
    r = requests.get(url, headers=headers).json()
    return r

def get_user_profile_from_group(group_id, user_id) -> dict:
    url = f'https://api.line.me/v2/bot/group/{group_id}/member/{user_id}'
    r = requests.get(url, headers=headers).json()
    return r

def get_message_file(message_id: str):
    url = f'https://api-data.line.me/v2/bot/message/{message_id}/content'
    r = requests.get(url, headers=headers)
    return r.content

def get_sticker_file(sticker_id: str, type_=str):
    if type_ == 'ANIMATION': url = f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{sticker_id}/iPhone/sticker_animation@2x.png'
    else: url = f'https://stickershop.line-scdn.net/stickershop/v1/sticker/{sticker_id}/android/sticker.png'
    r = requests.get(url, headers=headers)
    return r.content

def get_sticker_metadata(package_id: str):
    url = f'http://dl.stickershop.line.naver.jp/products/0/0/1/{package_id}/android/productInfo.meta'
    r = requests.get(url, headers=headers)
    return r.json()