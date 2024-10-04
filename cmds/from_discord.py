import io
import json
import requests
from pydub import AudioSegment
import discord
from discord.ext import commands
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage, SendMessage

from utils.Ltools import get_group_summary, get_user_profile
from core._cog import Cog_Extension


with open('config.json', 'r') as file:
    config = json.load(file)

line_bot_api = LineBotApi(config['LineBot']['ACCESS_TOKEN'])

class FromDiscord(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_channel(self, category_name, line_channel_id):
        category = discord.utils.get(self.bot.get_guild(config['DiscordBot']['guild_id']).categories, name=category_name)
        if category_name == 'Users':
            user_profile = get_user_profile(line_channel_id)
            chanel_name = user_profile['displayName']
        if category_name == 'Groups':
            group_summary = get_group_summary(line_channel_id)
            chanel_name = group_summary['groupName']
        new_channel = await category.create_text_channel(name=chanel_name)
        new_webhook = await new_channel.create_webhook(name=chanel_name)
        with open('data.json', 'r') as file:
            data = json.load(file)
        data[f'{"user" if category_name == "Users" else "group"}_table'][line_channel_id] = new_channel.id
        data['webhook_table'][new_channel.id] = new_webhook.url
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return new_channel

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        with open('data.json', 'r') as file:
            data = json.load(file)
        if msg.channel.id == data['logs_channel']['id'] and msg.author.name == 'Logs':
            message = msg.content.split()
            if message[0] == 'New':
                await self.create_channel(category_name=message[1][0].upper() + message[1][1:-1] + 's', line_channel_id=message[2])
            return
        
        if msg.author.bot: return

        with open('data.json', 'r') as file:
            data = json.load(file)
        if msg.channel.category.name == 'Users':
            channel_id = list(data['user_table'].keys())[list(data['user_table'].values()).index(msg.channel.id)]
        elif msg.channel.category.name == 'Groups':
            channel_id = list(data['group_table'].keys())[list(data['group_table'].values()).index(msg.channel.id)]

        if msg.content != '': line_bot_api.push_message(channel_id, TextSendMessage(text=msg.content))
        for attachment in msg.attachments:
            print(attachment.content_type)
            if attachment.content_type.startswith('image'):
                line_bot_api.push_message(channel_id, ImageSendMessage(original_content_url=attachment.url, preview_image_url=attachment.url))
            if attachment.content_type.startswith('video'):
                line_bot_api.push_message(channel_id, VideoSendMessage(original_content_url=attachment.url, preview_image_url=attachment.url))
            if attachment.content_type.startswith('audio'):
                audio = AudioSegment.from_file(io.BytesIO(requests.get(attachment.url, headers={'User-Agent': 'Mozilla/5.0'}).content))
                line_bot_api.push_message(channel_id, AudioSendMessage(original_content_url=attachment.url, duration=len(audio)))

async def setup(bot: commands.Bot):
    await bot.add_cog(FromDiscord(bot))