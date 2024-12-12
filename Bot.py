import discord
import asyncio  
import os
import random
discord.opus.load_opus('path_to_opus')
from discord.ext import commands


# Supported audio extensions
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac"}  # Add more as needed
COOLDOWN = 5  # Cooldown time in seconds between tracks


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) # can modify prefix for command if needed

# Path to the folder containing your mukbang audio files
AUDIO_FOLDER = "mukbang_audios"

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()  # Join the voice channel
        # Play random mukbang audio
        await play_random_audio_loop(vc)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:  # Check if the bot is in a voice channel
        await ctx.voice_client.disconnect()


async def play_random_audio_loop(vc):
    while True:  # Infinite loop to keep playing random audios
        # Get a list of valid audio files in the folder
        audio_files = [
            f for f in os.listdir("AUDIO FILE")
            if os.path.isfile(os.path.join("AUDIO FILE", f)) and os.path.splitext(f)[1] in AUDIO_EXTENSIONS
        ]
        
        if not audio_files:
            print("No valid audio files found in the folder!")
            await asyncio.sleep(COOLDOWN)  # Wait before retrying
            continue

        # Select a random audio file
        audio_file = random.choice(audio_files)
        audio_path = os.path.join("AUDIO FILE", audio_file)

        # Play the audio file
        print(f"Now playing: {audio_file}")
        vc.play(discord.FFmpegPCMAudio(source=audio_path))

        # Wait for the audio to finish playing
        while vc.is_playing():
            await asyncio.sleep(1)

        # Cooldown before playing the next audio
        print(f"Finished playing: {audio_file}. Waiting {COOLDOWN} seconds...")
        await asyncio.sleep(COOLDOWN)

bot.run("YOUR AUTH TOKEN")
