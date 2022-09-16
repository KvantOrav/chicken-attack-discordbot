
from discord import app_commands
from discord.ext import commands
import discord
import json
import typing
import datetime

from random import randint


with open("config.json", "r") as f:
    serverid = json.load(f)["server"]

class Birds(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded Birds")

    @app_commands.command()
    @app_commands.guilds(serverid)
    async def getbird(self, interaction, name: str):
        with open("birds.json", "r") as f:
            birds = json.load(f)
        birds[str(interaction.user.id)] = {"name": name, "hunger": 80, "colour": "black", "lastint": datetime.datetime.utcnow().timestamp(), "inventory": {"food": 1, "money": 0}}

        with open("birds.json", "w") as f:
            f.write(json.dumps(birds, indent=4))

        await interaction.response.send_message(f"{interaction.user.name} got a bird")


    @app_commands.command()
    @app_commands.guilds(serverid)
    async def shop(self, interaction, colours: typing.Optional[typing.Literal['red', 'green', 'blue']] = None):
        
        with open("birds.json", "r") as f:
            birds = json.load(f)

        class View(discord.ui.View):
            def __init__(self, birds):
                super().__init__(timeout=20)
                self.food = 20
                self.birds = birds
                
            async def interaction_check(self, interaction: discord.Interaction):
                if interaction.user == user:
                    return True
                else:
                    await interaction.response.send_message(
                        "You can't use that", ephemeral=True
                    )
                
            @discord.ui.button(label="Food", style=discord.ButtonStyle.blurple)
            async def food(self, interaction: discord.Interaction, button: discord.Button):
                money = self.birds[str(interaction.user.id)]["inventory"]["money"]
                if money < 1:
                    await interaction.response.send_message("Not enough money!", ephemeral=True)
                    return
                self.birds[str(interaction.user.id)]["inventory"]["money"] = money - 2
                self.birds[str(interaction.user.id)]["inventory"]["food"] = self.birds[str(interaction.user.id)]["inventory"]["food"] + 1
            @discord.ui.button(label="Colour", style=discord.ButtonStyle.blurple)
            async def colour(self, interaction: discord.Interaction, button: discord.Button):
                money = self.birds[str(interaction.user.id)]["inventory"]["money"]
                if money < 1:
                    await interaction.response.send_message("Not enough money!", ephemeral=True)
                else:
                    await interaction.response.send_message("Please buy directly using the slash command")


            @discord.ui.button(label="Name", style=discord.ButtonStyle.blurple)
            async def name(self, interaction: discord.Interaction, button: discord.Button):
                money = self.birds[str(interaction.user.id)]["inventory"]["money"]
                if money < 1:
                    await interaction.response.send_message("Not enough money!", ephemeral=True)
                    return
                
                class Modal(discord.ui.Modal):
                    def __init__(self, birds):
                        name = discord.ui.TextInput(label="New name")
                        super().__init__(title="Choose name")
                        self.add_item(name)
                        self.birds = birds

                    async def on_submit(self, interaction: discord.Interaction):
                        name = self.children[0].value
                        self.birds[str(interaction.user.id)]["inventory"]["money"] = money - 1
                        self.birds[str(interaction.user.id)]["name"] = name

                await interaction.response.send_modal(Modal(self.birds))


        user = interaction.user
        if str(user.id) not in birds:
            await interaction.response.send_message("you don't have a bird :(", ephemeral=True)
            return


        money = birds[str(user.id)]["inventory"]["money"]

        if colours:
            if money >= 1:
                birds[str(user.id)]["colour"] = colours
                await interaction.response.send_message(f"Your colour is now {colours}", ephemeral=True)
                with open("birds.json", "w") as f:
                    f.write(json.dumps(birds, indent=4))
                return
            else:
                await interaction.response.send_message(f"You don't have enough money", ephemeral=True)
                return

        embed = discord.Embed(title="Shop")
        embed.set_footer(text=f"You have {money} kurzbucks")
        embed.add_field(name="Food", value="2")
        embed.add_field(name="Colour", value="1")
        embed.add_field(name="Food", value="1")
        embed.add_field(name="Soap", value="soap")
        embed.add_field(name="Caretaker", value="100")
        view = View(birds)

        await interaction.channel.send(embed=embed, view=view)

    @commands.command()
    async def showbird(self, ctx):
        with open("birds.json", "r") as f:
            birds = json.load(f)

        class View(discord.ui.View):
            def __init__(self, birds):
                super().__init__(timeout=20)
                self.food = 20
                self.birds = birds
                
            async def on_timeout(self):
                for child in self.children:
                    child.disabled = True
                await message.edit(view=view)

            async def interaction_check(self, interaction: discord.Interaction):
                if interaction.user == user:
                    return True
                else:
                    await interaction.response.send_message(
                        "You can't use that", ephemeral=True
                    )
                
            @discord.ui.button(label="Feed", style=discord.ButtonStyle.blurple)
            async def feed(self, button: discord.Button, interaction: discord.Interaction):
                if self.birds[str(user.id)]["inventory"]["food"] <= 0:
                    await interaction.response.send_message("Out of food, buy more!", ephemeral=True)
                    return
                self.birds[str(user.id)]["inventory"]["food"] = self.birds[str(user.id)]["inventory"]["food"] - 1
                self.birds[str(user.id)]["hunger"] = self.birds[str(user.id)]["hunger"] + 1
                bird = self.birds[str(user.id)]
                embed = discord.Embed(title=bird["name"])
                embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/5/51/Mandarin.duck.arp.jpg")
                embed.add_field(name="Hunger", value=f'{bird["hunger"]}\nFood: {bird["inventory"]["food"]}')

                with open("birds.json", "w") as f:
                    f.write(json.dumps(self.birds, indent=4))
                
                await message.edit(embed=embed, view=view)

            @discord.ui.button(label="Play", style=discord.ButtonStyle.blurple)
            async def play(self, button: discord.Button, interaction: discord.Interaction):
                await interaction.response.send_message("No play yet!", ephemeral=True)

            @discord.ui.button(label="Medicine", style=discord.ButtonStyle.blurple)
            async def medicine(self, button: discord.Button, interaction: discord.Interaction):
                await interaction.response.send_message("Bankruptcy!", ephemeral=True)


        user = ctx.author
        if str(user.id) not in birds:
            await ctx.reply("you don't have a bird :(")
            return
        bird = birds[str(user.id)]

        hunger = int((datetime.datetime.utcnow().timestamp() - bird["lastint"])/20)

        birds[str(user.id)]["hunger"] = birds[str(user.id)]["hunger"] - hunger

        birds[str(user.id)]["lastint"] = datetime.datetime.utcnow().timestamp()

        embed = discord.Embed(title=bird["name"])
        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/5/51/Mandarin.duck.arp.jpg")
        embed.add_field(name="Hunger", value=f'{bird["hunger"]}\nFood: {birds[str(user.id)]["inventory"]["food"]}')
        if bird["colour"] == "black":
            embed.colour = discord.Colour.default()
        if bird["colour"] == "red":
            embed.colour = discord.Colour.red()
        if bird["colour"] == "green":
            embed.colour = discord.Colour.green()
        if bird["colour"] == "blue":
            embed.colour = discord.Colour.blue()
        food = bird["hunger"]
        view = View(birds)
        
        with open("birds.json", "w") as f:
            f.write(json.dumps(birds, indent=4))

        message = await ctx.send(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Birds(bot))