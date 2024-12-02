import discord
from discord.ext import commands
from discord import app_commands
import google.generativeai as genai
from discord import FFmpegPCMAudio
from yt_dlp import YoutubeDL
import os
from discord import PCMVolumeTransformer

# Import bot token
from apikeys import *

# Set up Google GenAI API key
genai.configure(api_key=geminiToken)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

        try:
            guild = discord.Object(id = 1122501766894846044)
            synced = await self.tree.sync(guild = guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
            print('-------------------------------------------------------')

        except Exception as e:
            print(f'Error syncing commands: {e}')

# Define the intents
intents = discord.Intents.default()  # Enables default intents 
intents.message_content = True  # Enable access to message content 
client = Client(command_prefix='!', intents=intents)  # Initialize the bot with the command prefix and intents

GUILD_ID = discord.Object(id = 1122501766894846044)

# Hello Command
@client.tree.command(name = "hello", description = "Say Hello!", guild=GUILD_ID)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, I'm Andronel!")


# Gemini Integration
@client.tree.command(name="ask", description="Ask Gemini a question", guild=GUILD_ID)
async def ask(interaction: discord.Interaction, question: str):
    """Handle user queries and pass them to Gemini's API."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")   # Create an instance of the Gemini model
        response = model.generate_content(question) # Generate a response using the Gemini model
        answer = response.text  # Extract the text of the response

        # Check if the response exceeds Discord's message limit (2000 characters)
        if len(answer) > 2000:
            # Split the response into chunks of 2000 characters
            chunks = [answer[i:i+2000] for i in range(0, len(answer), 2000)]
            for chunk in chunks:
                await interaction.response.send_message(chunk)  # Send each chunk as a separate message
        else:
            await interaction.response.send_message(answer)  # Send the response if it's under 2000 characters
    
    except Exception as e:
        # Handle any errors
        await interaction.response.send_message("Sorry, I couldn't process your request. Please try again later!")
        print(f"Error: {e}")


# Voice Join
@client.tree.command(name="androjoin", description="Join a voice channel", guild=GUILD_ID)
async def voiceJoin(interaction: discord.Interaction):
    if interaction.user.voice:
        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message("Joined the voice channel!")
    else:
        await interaction.response.send_message("You're not in a voice channel. You must be in a voice channel to run this command.")

# Voice Leave
@client.tree.command(name="androleave", description="Leave the voice channel", guild=GUILD_ID)
async def voiceLeave(interaction: discord.Interaction):
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("I've left the voice channel.")
    else:
        await interaction.response.send_message("I am not in a voice channel.")


# Music Integration via YouTube
@client.tree.command(name="play", description="Play a song from YouTube", guild=GUILD_ID)
@app_commands.describe(title="The title of the song to play")
async def play(interaction: discord.Interaction, title: str):
    try:
        # Defer the interaction response as response takes longer than 3 seconds
        await interaction.response.defer()  # Sends an "acknowledgment" that the bot is processing

        # Check if the user is in a voice channel
        if not interaction.user.voice:
            await interaction.response.send_message("You're not in a voice channel. You must be in a voice channel to run this command.")
            return

        channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await channel.connect()

        voice = interaction.guild.voice_client

        ytdl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'postprocessors': [{'key': 'FFmpegFixupM4a'}],
        }

        with YoutubeDL(ytdl_opts) as ydl:
            search_query = f"ytsearch:{title.replace(' ', '+')}"
            info = ydl.extract_info(search_query, download=False)

            if 'entries' in info and len(info['entries']) > 0:
                video_url = info['entries'][0]['url']
                video_title = info['entries'][0]['title']
            else:
                await interaction.followup.send("No results found for that song title.")
                return

        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        source = PCMVolumeTransformer(FFmpegPCMAudio(video_url, **ffmpeg_opts))

        if voice.is_playing():
            voice.pause()

        voice.play(source, after=lambda e: print(f"Finished playing: {video_title}"))
        await interaction.followup.send(f"Now playing: **{video_title}**")

    except Exception as e:
        await interaction.followup.send("An error occurred while trying to play the song.")
        print(f"Error in play command: {e}")


# Pause
@client.tree.command(name="pause", description="Pause the current song", guild=GUILD_ID)
async def pause(interaction: discord.Interaction):
    voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice and voice.is_playing():
        voice.pause()
        await interaction.response.send_message("Playback paused")
    else:
        await interaction.response.send_message("There's nothing to pause")

# Resume
@client.tree.command(name="resume", description="Resume playback", guild=GUILD_ID)
async def resume(interaction: discord.Interaction):
    voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
    if voice and voice.is_paused():
        voice.resume()
        await interaction.response.send_message("Playback resumed")
    else:
        await interaction.response.send_message("The song is already playing")


  
# Run the Bot
client.run(botToken)

