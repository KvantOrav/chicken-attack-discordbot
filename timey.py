
from discord.ext import tasks, commands
import discord
import json
import datetime

from random import randint


with open("config.json", "r") as f:
    serverid = json.load(f)["server"]

class Timey(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded Time")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open("birds.json", "r") as f:
            birds = json.load(f)
        if str(message.author.id) in birds:
            birds[str(message.author.id)]["inventory"]["money"] += 1
            
        with open("birds.json", "w") as f:
            f.write(json.dumps(birds, indent=4))

        if message.channel.id != 952581316690477079:
            return

        if not randint(0, 100):
            await message.channel.send("A wild moderator appeared, quick hide the evidence!")
        if not randint(0, 1000):
            await message.channel.send("Your pet is sick!! (not really)")

    @tasks.loop(hours=24)
    async def giveaway_task(self):
        pass

    @tasks.loop(hours=1)
    async def giveaway_task(self):
        pass


async def setup(bot):
    await bot.add_cog(Timey(bot))