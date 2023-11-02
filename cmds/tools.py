import json
import discord
from discord.ext import commands

from core._cog import Cog_Extension

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


async def setup(bot: commands.Bot):
    await bot.add_cog(Tools(bot))