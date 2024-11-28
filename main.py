import discord
from discord.ext import commands

# import bot token
from apikeys import *

# Define the intents
intents = discord.Intents.default()  # Enables default intents (guilds, messages, etc.)
intents.message_content = True  # Enable access to message content (required in discord.py 2.x)

# Initialize the bot with the command prefix and intents
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is Ready")
    print("---------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm Andronel!")

client.run(botToken)

