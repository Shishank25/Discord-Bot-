import discord
from discord.ext import commands
from discord.utils import get
from discord import Intents, Client, Message, FFmpegPCMAudio
import yt_dlp
from views.musicview import MusicView
from utils.youtube import search_youtube
import asyncio

intents: Intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client: Client = commands.Bot(command_prefix="!", intents=intents)

song_q = {}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 48000 -b:a 192k'}


async def play_next(guild, message):
    print('play next begins')
    voice_client = message.guild.voice_client
    guild_id = message.guild.id
    print(f"message.guild: {message.guild}")
    print(f"client.voice_clients: {client.voice_clients}")


    if voice_client is None:
        await message.channel.send("I'm not connected to a voice channel.")
        return

    
    print('play next is working')
    next_song = song_q[guild_id].pop(0)
    bot_loop = asyncio.get_event_loop()
    voice_client.play(discord.FFmpegPCMAudio(next_song['url'], **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(play_next(guild, message), bot_loop))
    await message.channel.send(f'Now Playing: {next_song['title']}')
    view = MusicView(guild, message, song_q)
    await message.channel.send("Control the music:", view=view)


    if not song_q[guild_id]:
        await message.channel.send('Query is empty!')
        return


async def play_song(message, query):
    # if message.guild.voice_client:  
    voice_client = message.guild.voice_client
    channel = message.author.voice.channel
    guild_id = message.guild.id
    print(f"message.guild: {message.guild}")
    print(f"client.voice_clients: {client.voice_clients}")

    print(f"Message: {message.content}, Guild: {message.guild.id}, Author: {message.author}")

    if guild_id not in song_q:
        song_q[guild_id] = []


    if not voice_client:
        await channel.connect()
    
    song_info = search_youtube(query)

    if song_info is None:
        await message.channel.send("Song not found.")
        return

    if voice_client and voice_client.is_playing():
        song_q[guild_id].append(song_info)
        await message.channel.send('Song Added to Queue!')

    else:
        song_q[guild_id].append(song_info)
        await play_next(message.guild, message)

    print('play song works')
        


async def pause_song(message):
    voice_client = message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await message.channel.send("Playback paused.")
    else:
        await message.channel.send("No audio is currently playing.")


async def resume_song(message):
    voice_client = message.guild.voice_client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await message.channel.send("Playback resumed.")
    else:
        await message.channel.send("No audio is currently paused.")