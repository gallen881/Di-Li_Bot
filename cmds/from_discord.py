import io
import json
from pydub import AudioSegment
import discord
from discord.ext import commands
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, VideoSendMessage, AudioSendMessage, SendMessage

from utils.Dtools import get_file
from core._cog import Cog_Extension


with open('config.json', 'r') as file:
    config = json.load(file)

line_bot_api = LineBotApi(config['LineBot']['ACCESS_TOKEN'])

class FromDiscord(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
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
                audio = AudioSegment.from_file(io.BytesIO(get_file(attachment.url)))
                line_bot_api.push_message(channel_id, AudioSendMessage(original_content_url=attachment.url, duration=len(audio)))


async def setup(bot: commands.Bot):
    await bot.add_cog(FromDiscord(bot))