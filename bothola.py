import discord
from discord.ext import commands


intents= discord.Intents.all()

bot=commands.Bot(
    command_prefix="!",
    description="Bot Recordador de eventos",
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Bot conectado {len(bot.guilds)} ")

@bot.event
async def on_message(message):
    print("message:", message)
    print(f"USER-{message.author}texted - {message.content}")
    await bot.process_commands(message)



@bot.command()
async def saludar(ctx):
    print("comando recivido")
    await ctx.send("Holaaa")

bot.run("Token")
