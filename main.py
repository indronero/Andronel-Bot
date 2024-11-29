import discord
from discord.ext import commands
import google.generativeai as genai

# Import bot token
from apikeys import *

# Set up Google GenAI API key
genai.configure(api_key=geminiToken)

# Define the intents
intents = discord.Intents.default()  # Enables default intents 
intents.message_content = True  # Enable access to message content 

# Initialize the bot with the command prefix and intents
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print("Bot is Ready")
    print("--------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I'm Andronel!")

# Gemini Integration
@client.command()
async def ask(ctx, *, question):
    """Handle user queries and pass them to Gemini's API."""
    try:
        # Create an instance of the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        # Generate a response using the Gemini model
        response = model.generate_content(question)
        # Extract the text of the response
        answer = response.text

        # Check if the response exceeds Discord's message limit (2000 characters)
        if len(answer) > 2000:
            # Split the response into chunks of 2000 characters
            chunks = [answer[i:i+2000] for i in range(0, len(answer), 2000)]
            for chunk in chunks:
                await ctx.send(chunk)  # Send each chunk as a separate message
        else:
            await ctx.send(answer)  # Send the response if it's under 2000 characters
    
    except Exception as e:
        # Handle any errors
        await ctx.send("Sorry, I couldn't process your request. Please try again later!")
        print(f"Error: {e}")

# Voice join 
@client.command(pass_context = True)
async def androjoin(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You're not in a voice channel. You must be in a voice channel to run this command")

# Voice leave
@client.command(pass_context = True)
async def androleave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I've left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")

  
# Run the Bot
client.run(botToken)

