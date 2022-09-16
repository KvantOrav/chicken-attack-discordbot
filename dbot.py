with open("token.txt", "r") as f:
    token = f.read()

import discord
from discord import app_commands
from discord.ext import commands

from typing import List, Union, Optional

import asyncio

import json

with open("config.json", "r") as f:
    serverid = json.load(f)["server"]

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


bot = Bot()

@bot.command()
async def reload(ctx: commands.Context, cog):
    """Reloads commands."""
    try:
        await bot.reload_extension(cog)
        print("reloaded " + cog)
    except:
        await ctx.reply("No " + cog)
    

@bot.command()
async def register(ctx: commands.Context):
    """Syncs slash commands."""
    await bot.tree.sync(guild=discord.Object(id=serverid))



async def main():
    async with bot:
        await bot.load_extension("birds")
        await bot.load_extension("fight")
        await bot.load_extension("timey")
        await bot.start(token, reconnect=True)

asyncio.run(main())