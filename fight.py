
from turtle import setundobuffer
from discord import app_commands
from discord.ext import commands
import discord
import json

import datetime

from random import randint

import copy

import json

with open("config.json", "r") as f:
    serverid = json.load(f)["server"]

class Fight(commands.Cog):
    def __init__(self, bot):
        with open("birds.json", "r") as f:
            birds = json.load(f)
        self.birds = birds

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded Fight")


    @app_commands.command()
    @app_commands.guilds(serverid)
    async def fight(self, interaction: discord.Interaction, member: discord.Member):
        class View(discord.ui.View):
            def __init__(self, fighters, fighter1, fighter2):
                super().__init__(timeout=30)
                self.fightingbirds = fighters
                self.fighters = (fighter1, fighter2)
                self.currentturn = 0
                self.fleed = False
                
            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await message.edit(view=view)

            async def interaction_check(self, interaction: discord.Interaction):
                if interaction.user in self.fighters:
                    if interaction.user == self.fighters[self.currentturn]:
                        return True
                    else:
                        await interaction.response.send_message("Not your turn", ephemeral=True)
                else:
                    await interaction.response.send_message("You can't use that", ephemeral=True)

            async def gamelogic(self, action):
                self.currentturn = int(not self.currentturn)
                if action == "attack1":
                    damage = randint(5, 10)
                    self.fightingbirds[self.currentturn]["health"] -= damage
                    self.fightingbirds[int(not self.currentturn)]["stamina"] -= 15
                elif action == "attack2":
                    damage = randint(3, 5)
                    self.fightingbirds[self.currentturn]["health"] -= damage
                    self.fightingbirds[int(not self.currentturn)]["stamina"] -= 8
                elif action == "defend":
                    self.fightingbirds[int(not self.currentturn)]["stamina"] += 13

                if self.fightingbirds[self.currentturn]["health"] <= 0:
                    embed = discord.Embed(title="WINNER!!!!", description=f"{self.fighters[int(not self.currentturn)].mention} won!")
                    embed.add_field(name=self.fightingbirds[0]["name"], value=f"Health: {self.fightingbirds[0]['health']}")
                    embed.add_field(name=self.fightingbirds[1]["name"], value=f"Health: {self.fightingbirds[1]['health']}")
                    await message.edit(embed=embed, view=None)
                    return

                if self.fightingbirds[self.currentturn]["stamina"] in range(8, 14):
                    for child in self.children:
                        if child.label == "Attack 1":
                            child.disabled = True
                elif self.fightingbirds[self.currentturn]["stamina"] < 8:
                    for child in self.children:
                        if child.label == "Attack 1":
                            child.disabled = True
                        if child.label == "Attack 2":
                            child.disabled = True
                else:
                    for child in self.children:
                        child.disabled = False

                embed = discord.Embed(title="FIGHT!!!!", description=f"{self.fighters[self.currentturn].mention} turn")
                embed.add_field(name=self.fightingbirds[0]["name"], value=f"Health: {self.fightingbirds[0]['health']}\nStamina: {self.fightingbirds[0]['stamina']}")
                embed.add_field(name=self.fightingbirds[1]["name"], value=f"Health: {self.fightingbirds[1]['health']}\nStamina: {self.fightingbirds[1]['stamina']}")

                if action == "flee":
                    for child in self.children:
                        if child.label == "Flee":
                            child.label = "Mercy"
                            child.style = discord.ButtonStyle.green
                    embed = discord.Embed(title="Fight?", description=f"Does {self.fighters[self.currentturn].mention} want to show mercy or win this fight?")

                if self.fleed:
                    if action == "flee":
                        embed = discord.Embed(title="Mercy", description=f"Mercy")
                    else:
                        embed = discord.Embed(title="Winner", description=f"{self.fighters[int(not self.currentturn)].mention} won!")
                    

                await message.edit(embed=embed, view=view)
                

            @discord.ui.button(label="Attack 1", style=discord.ButtonStyle.blurple)
            async def attack1(self, interaction: discord.Interaction, button: discord.Button):
                await self.gamelogic("attack1")

            @discord.ui.button(label="Attack 2", style=discord.ButtonStyle.blurple)
            async def attack2(self, interaction: discord.Interaction, button: discord.Button):
                await self.gamelogic("attack2")

            @discord.ui.button(label="Defend", style=discord.ButtonStyle.green)
            async def defend(self, interaction: discord.Interaction, button: discord.Button):
                await self.gamelogic("defend")

            @discord.ui.button(label="Flee", style=discord.ButtonStyle.danger)
            async def flee(self, interaction: discord.Interaction, button: discord.Button):
                await self.gamelogic("flee")

        fighters = ({"name": self.birds[str(interaction.user.id)]["name"], "health": 20, "stamina": 30}, {"name": self.birds[str(member.id)]["name"], "health": 20, "stamina": 30})

        embed = discord.Embed(title="FIGHT!!!!", description=f"{interaction.user.mention} turn")
        embed.add_field(name=fighters[0]["name"], value=f"Health: {fighters[0]['health']}\nStamina: {fighters[0]['stamina']}")
        embed.add_field(name=fighters[1]["name"], value=f"Health: {fighters[1]['health']}\nStamina: {fighters[1]['stamina']}")

        view = View(fighters, interaction.user, member)

        message = await interaction.channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"{member.name} no fight yet!", ephemeral=True)

    
    @commands.command()
    async def worms(self, ctx):
        class ViewWorms(discord.ui.View):
            def __init__(self, wormcoord, treecoord, bombcoord):
                super().__init__(timeout=30)
                self.move = (0, 0)
                self.coord = [2, 4]

                self.wormcoord = wormcoord
                self.treecoord = treecoord
                self.bombcoord = bombcoord

                self.draw()

            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await message.edit(view=view)

            '''async def interaction_check(self, interaction: discord.Interaction):
                if interaction.user == ctx.author:
                    return
                else:
                    await interaction.response.send_message("You can't use that", ephemeral=True)'''

            def gaming(self, move):
                newcoord = copy.deepcopy(self.coord)
                newcoord[move[1]] += move[0]
                canmove = True
                if newcoord == self.treecoord:
                    canmove = False

                if newcoord[move[1]] in range(5) and canmove:
                    self.coord = newcoord
                    if self.coord == self.wormcoord:
                        self.wormcoord = None

                    if self.coord == self.bombcoord:
                        self.bombcoord = None
                
                    return self.draw()
            
            def draw(self):
                board = ""
                for y in range(5):
                    for x in range(5):
                        if [x, y] == self.coord:
                            board += ":bird:"
                        elif [x,y] == self.wormcoord:
                            board += ":worm:"
                        elif [x, y] == self.treecoord:
                            board += ":deciduous_tree:"
                        elif [x, y] == self.bombcoord:
                            board += ":bomb:"                               
                        else:
                            board += ":black_large_square:"
                    board += "\n"

                if self.wormcoord == None:
                    board = "YOU ATE THE WORM!!"

                if self.bombcoord == None:
                    board = "YOU BLEW UP!!"

                embed = discord.Embed(title="Worms worms worms", description=board)
                
                if self.bombcoord == None:
                    embed.set_image(url="https://c.tenor.com/mjm5lfGFIuEAAAAC/look-what-you-fucking-did.gif")

                return embed


            #coordinates are (movement, axis)
            @discord.ui.button(label=" ", style=discord.ButtonStyle.gray, row=0, disabled=True)
            async def empty1(self, interaction: discord.Interaction, button: discord.Button):
                self.move = 1

            @discord.ui.button(emoji="⬆️", style=discord.ButtonStyle.gray, row=0)
            async def up(self, interaction: discord.Interaction, button: discord.Button):
                embed = self.gaming((-1, 1))
                if embed != None:
                    await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Can't do that!", ephemeral=True)
            
            @discord.ui.button(label=" ", style=discord.ButtonStyle.gray, row=0, disabled=True)
            async def empty2(self, interaction: discord.Interaction, button: discord.Button):
                self.move = 1

            @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.gray, row=1)
            async def left(self, interaction: discord.Interaction, button: discord.Button):
                embed = self.gaming((-1, 0))
                if embed != None:
                    await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Can't do that!", ephemeral=True)

            @discord.ui.button(label=" ", style=discord.ButtonStyle.gray, row=1, disabled=True)
            async def empty3(self, interaction: discord.Interaction, button: discord.Button):
                self.move = 1

            @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.gray, row=1)
            async def right(self, interaction: discord.Interaction, button: discord.Button):
                embed = self.gaming((1, 0))
                if embed != None:
                    await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Can't do that!", ephemeral=True)

            @discord.ui.button(label=" ", style=discord.ButtonStyle.gray, row=2, disabled=True)
            async def empty4(self, interaction: discord.Interaction, button: discord.Button):
                self.move = 1

            @discord.ui.button(emoji="⬇️", style=discord.ButtonStyle.gray, row=2)
            async def down(self, interaction: discord.Interaction, button: discord.Button):
                embed = self.gaming((1, 1))
                if embed != None:
                    await interaction.response.edit_message(embed=embed)
                else:
                    await interaction.response.send_message("Can't do that!", ephemeral=True)

            @discord.ui.button(label=" ", style=discord.ButtonStyle.gray, row=2, disabled=True)
            async def empty5(self, interaction: discord.Interaction, button: discord.Button):
                self.move = 1

        coord = [2, 4]

        wormcoord = [randint(0, 4), randint(0, 4)]
        treecoord = [randint(0, 4), randint(0, 4)]
        bombcoord = [randint(0, 4), randint(0, 4)]

        board = ""
        for y in range(5):
            for x in range(5):
                if [x, y] == coord:
                    board += ":bird:"
                elif [x, y] == wormcoord:
                    board += ":worm:"
                elif [x, y] == treecoord:
                    board += ":deciduous_tree:"
                elif [x, y] == bombcoord:
                    board += ":bomb:"
                else:
                    board += ":black_large_square:"

            board += "\n"

        embed = discord.Embed(title="Worms worms worms", description=board)

        view = ViewWorms(wormcoord, treecoord, bombcoord)

        message = await ctx.send(embed=embed, view=view)



async def setup(bot):
    await bot.add_cog(Fight(bot))