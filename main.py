import discord
from discord.ext import commands
import google.generativeai as genai
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import os
from discord import PCMVolumeTransformer

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

# Music Integration via Youtube
@client.command(pass_context = True)
async def play(ctx, *, title: str):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        # Connect to the voice channel if not already connected
        if ctx.voice_client is None:
            await channel.connect()

        voice = ctx.voice_client

        # yt-dlp options for streaming
        ytdl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegFixupM4a',
            }],
            # Save the downloaded file in the 'downloads/songs' directory
            'outtmpl': 'downloads/songs/%(title)s.%(ext)s',  
        }

         # Use yt-dlp to search for the song by title
        with YoutubeDL(ytdl_opts) as ydl:
            search_query = f"ytsearch:{title.replace(' ', '+')}"  # Prefix the title with 'ytsearch:' to search on YouTube (Replace ' ' with '+' as yt-dlp throws minor search error)
            info = ydl.extract_info(search_query, download=False)

            # Get the URL of the best result (first item in the list of search results)
            if 'entries' in info and len(info['entries']) > 0:
                video_url = info['entries'][0]['url']
                video_title = info['entries'][0]['title']
            else:
                await ctx.send("No results found for that song title.")
                return

        # Use FFmpegPCMAudio with additional options for buffering as stream is ending prematurely
        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  # Reconnect options for streaming
            'options': '-vn',  # Ensure video is not being processed (only audio)
        }

        # Wrap in PCMVolumeTransformer for better volume control
        source = PCMVolumeTransformer(FFmpegPCMAudio(video_url, **ffmpeg_opts))

        if voice.is_playing():
            voice.pause()

        voice.play(source, after=lambda e: print(f"Finished playing: {video_title}"))
        await ctx.send(f"Now playing: **{video_title}**")
    else:
        await ctx.send("You're not in a voice channel. You must be in a voice channel to run this command")    


@client.command(pass_context = True)
async def pause(ctx):  
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)  
    if voice.is_playing():
        voice.pause()
        await ctx.send("Playback Paused")
    else:
        await ctx.send("There is no song playing")

@client.command(pass_context = True)
async def resume(ctx):  
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)  
    if voice.is_paused():
        voice.resume()
        await ctx.send("Playback Resumed")
    else:
        await ctx.send("There is no song paused")


  
# Run the Bot
client.run(botToken)

