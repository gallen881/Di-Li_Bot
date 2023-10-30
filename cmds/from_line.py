import json
import asyncio
import discord
from discord.ext import commands

from core._cog import Cog_Extension
from utils.Ltools import get_group_summary, get_user_profile


with open('config.json', 'r') as file:
    config = json.load(file)
with open('data.json', 'r') as file:
    data = json.load(file)


class FromLine(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def checker():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                with open('switcher.json', 'r') as file:
                    switcher = json.load(file)
                if data['last_timestamp']['message'] != switcher['message']['timestamp']:
                    data['last_timestamp']['message'] = switcher['message']['timestamp']
                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    await self.send_text(switcher['message'])
                if data['last_timestamp']['join'] != switcher['join']['timestamp']:
                    data['last_timestamp']['join'] = switcher['join']['timestamp']
                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    await self.welcome_joining(switcher['join'])
                    
                await asyncio.sleep(1)

        self.bot.loop.create_task(checker())

    async def create_group_channel(self, sdata: dict) -> discord.TextChannel:
        group_summary = get_group_summary(sdata['groupId'])
        guild = self.bot.get_guild(config['DiscordBot']['guild_id'])
        category = discord.utils.get(guild.categories, name='Groups')
        channel = await guild.create_text_channel(name=group_summary['groupName'], category=category)
        data['group_table'][sdata['groupId']] = channel.id
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        return channel

    async def send_text(self, sdata: dict):
        user_profile = get_user_profile(sdata['userId'])
        if sdata['groupId'] is None:
            if sdata['userId'] not in data['user_table'].keys():
                guild = self.bot.get_guild(config['DiscordBot']['guild_id'])
                category = discord.utils.get(guild.categories, name='Users')
                channel = await guild.create_text_channel(name=user_profile['displayName'], category=category)
                data['user_table'][sdata['userId']] = channel.id
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            else:
                channel_id = data['user_table'][sdata['userId']]
                channel = self.bot.get_channel(channel_id)
            msg = sdata['text']

        else:
            if sdata['groupId'] not in data['group_table'].keys():
                channel = await self.create_group_channel(sdata)
            else:
                channel_id = data['group_table'][sdata['groupId']]
                channel = self.bot.get_channel(channel_id)
            msg = f'**{user_profile["displayName"]}: **\n{sdata["text"]}'.replace('\n', '\n> ')

        await channel.send(msg)

    async def welcome_joining(self, sdata: dict):
        group_name = get_group_summary(sdata['groupId'])['groupName']
        if sdata['groupId'] not in data['group_table'].keys():
            channel = await self.create_group_channel(sdata)
        else:
            channel_id = data['group_table'][sdata['groupId']]
            channel = self.bot.get_channel(channel_id)
        await channel.send(f'***System Info: ***\n> Into {group_name}!')

async def setup(bot: commands.Bot):
    await bot.add_cog(FromLine(bot))