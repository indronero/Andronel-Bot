import discord
from discord.ext import commands
'''import openai'''

# import bot token
from apikeys import *

'''openai.api_key = gptToken'''

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

'''
@client.command()
async def ask(ctx, *, question):
    """Handle user queries and pass them to OpenAI's API."""
    try:
        # Call OpenAI API with the user's question
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  
            messages=[{"role": "user", "content": question}],
            max_tokens=150,  # Limit the response length
            temperature=0.7,  # Adjust creativity of the response
        )
        
        # Extract the generated text from OpenAI's response
        answer = response.choices[0].message.content.strip()
        
        # Send the response back to Discord
        await ctx.send(answer)
    
    except Exception as e:
        # Handle any errors
        await ctx.send("Sorry, I couldn't process your request. Please try again later!")
        print(f"Error: {e}")
    '''
@client.command(pass_context = True)
async def androjoin(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You're not in a voice channel. You must be in a voice channel to run this command")

@client.command(pass_context = True)
async def androleave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I've left the voice channel")
    else:
        await ctx.send("I am not in a voice channel")


    

client.run(botToken)

