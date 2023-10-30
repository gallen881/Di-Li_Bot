import os
import asyncio
import json
import discord
from discord.ext import commands

from utils.Dtools import print_detail

with open('config.json', 'r') as file:
    config = json.load(file)

bot = commands.Bot(command_prefix=config['DiscordBot']['prefix'], intents=discord.Intents.all())

async def main():
    @bot.event
    async def on_ready():
        print_detail('INFO', obj='Discord Bot is ready')
    
    @bot.command()
    @commands.is_owner()
    async def load(ctx: commands.Context, extension):
        await bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension} successfully')
        print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py loaded successfully')


    @bot.command(aliases=['ul'])
    @commands.is_owner()
    async def unload(ctx: commands.Context, extension):
        await bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Unloaded {extension} successfully')
        print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py unloaded successfully')


    @bot.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(ctx: commands.Context, extension):
        await bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reloaded {extension} successfully')
        print_detail(memo='INFO', user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py reloaded successfully')

    async with bot:
        for file in os.listdir('./cmds'):
            if file.endswith('.py'):
                await bot.load_extension(f'cmds.{file[:-3]}')
                print_detail(memo='INFO', obj=f'{file} loaded successfully')
        await bot.start(config['DiscordBot']['token'])

asyncio.run(main())