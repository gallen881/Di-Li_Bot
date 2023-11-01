import json
import discord
from discord.ext import commands
from linebot import LineBotApi
from linebot.models import TextSendMessage

from core._cog import Cog_Extension


with open('config.json', 'r') as file:
    config = json.load(file)
with open('data.json', 'r') as file:
    data = json.load(file)

line_bot_api = LineBotApi(config['LineBot']['ACCESS_TOKEN'])

class FromDiscord(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.author.bot:
            return
        with open('data.json', 'r') as file:
            data = json.load(file)
        if msg.channel.category.name == 'Users':
            user_id = list(data['user_table'].keys())[list(data['user_table'].values()).index(msg.channel.id)]
            line_bot_api.push_message(user_id, TextSendMessage(text=msg.content))
        elif msg.channel.category.name == 'Groups':
            group_id = list(data['group_table'].keys())[list(data['group_table'].values()).index(msg.channel.id)]
            line_bot_api.push_message(group_id, TextSendMessage(text=msg.content))

async def setup(bot: commands.Bot):
    await bot.add_cog(FromDiscord(bot))