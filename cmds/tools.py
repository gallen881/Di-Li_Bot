import json
import discord
from discord.ext import commands

from core._cog import Cog_Extension
from utils.Ltools import get_group_summary, get_user_profile

with open('config.json', 'r') as file:
    config = json.load(file)


class Tools(Cog_Extension):
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'ping: {round(self.bot.latency * 1000, 2)} (ms)')

    @commands.command()
    async def setup(self, ctx: commands.Context):
        guild = self.bot.get_guild(config['DiscordBot']['guild_id'])
        assert guild == ctx.guild, 'Please use this command in the guild that you entered in the config file.'
        await guild.create_category(name='Groups')
        await guild.create_category(name='Users')
        await ctx.send('Setup done.')

    @commands.command()
    async def update(self, ctx: commands.Context):
        with open('data.json', 'r') as file:
            data = json.load(file)
        for user_id, channel_id in data['user_table'].items():
            channel = self.bot.get_channel(channel_id)
            user_name = get_user_profile(user_id)['displayName']
            if channel.name != user_name:
                await ctx.send(f'Change {channel.name} to {user_name}')
                await channel.edit(name=user_name)
        for group_id, channel_id in data['group_table'].items():
            channel = self.bot.get_channel(channel_id)
            group_name = get_group_summary(group_id)['groupName']
            if channel.name != group_name:
                await ctx.send(f'Change {channel.name} to {group_name}')
                await channel.edit(name=group_name)

        await ctx.send('Update done.')


async def setup(bot: commands.Bot):
    await bot.add_cog(Tools(bot))