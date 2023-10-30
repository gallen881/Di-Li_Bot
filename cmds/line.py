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


class Line(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def checker():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                with open('switcher.json', 'r') as file:
                    switch_data = json.load(file)
                if data['last_timestamp'] != switch_data['timestamp']:
                    # print(22)
                    data['last_timestamp'] = switch_data['timestamp']
                    with open('data.json', 'w') as file:
                        json.dump(data, file, indent=4)
                    await self.send_text(switch_data)

                await asyncio.sleep(1)

        self.bot.loop.create_task(checker())


    async def send_text(self, sdata: dict):
        user_profile = get_user_profile(sdata['userId'])
        if sdata['groupId'] is None:
            if sdata['userId'] not in data['user_table'].keys():
                channel = await self.bot.get_guild(config['DiscordBot']['guild_id']).create_text_channel(name=user_profile['displayName'])
                data['user_table'][sdata['userId']] = channel.id
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            else:
                channel_id = data['user_table'][sdata['userId']]
                channel = self.bot.get_channel(channel_id)
            msg = sdata['text']

        else:
            if sdata['groupId'] not in data['group_table'].keys():
                group_summary = get_group_summary(sdata['groupId'])
                channel = await self.bot.get_guild(config['DiscordBot']['guild_id']).create_text_channel(name=group_summary['groupName'])
                data['group_table'][sdata['groupId']] = channel.id
                with open('data.json', 'w') as file:
                    json.dump(data, file, indent=4)
            else:
                channel_id = data['group_table'][sdata['groupId']]
                channel = self.bot.get_channel(channel_id)
            msg = f'**{user_profile["displayName"]}: **\n> {sdata["text"]}'

        await channel.send(msg)

async def setup(bot: commands.Bot):
    await bot.add_cog(Line(bot))