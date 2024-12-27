from typing import Final
import os
import asyncio
import pyttsx3
from dotenv import load_dotenv
from discord import Intents, Client, Message, FFmpegPCMAudio
import discord
from discord.utils import get
from discord.ext import commands
from utils.response import get_response, get_response1
import yt_dlp
from views.musicview import MusicView
from commands.music import play_next, play_song, resume_song, pause_song, song_q
from commands.general import cmnds, join_channel, leave_channel, speak_message
from utils.utils import text_to_speech, parse_time

#------Initialize and Configure the pyttsx3 library for text-to-speech conversion--------# 
engine = pyttsx3.init()                         # Initialize the text to speech engine
engine.setProperty('rate', 150)                 # Adjust speaking speed (default: 200)
engine.setProperty('volume', 0.50)              # Adjust volume (0.0 to 1.0)


load_dotenv()
TOKEN: Final[str] = os.getenv('discord_token')
allowed_channel_id = [1283533822012424332,1285288807297581109]
specific_user_id = 850061033921970177

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 48000 -b:a 192k'}

intents: Intents = discord.Intents.default()    # Creates a default set of intents that the bot will listen to
intents.message_content = True                  # Allows the bot to receive the contents inside a message  
intents.guilds = True                           # Allows the bot to receive updates about guilds (servers)

#-----Create an instance of the class commands.bot .Bot with the specified token and intents-----#
client: Client = commands.Bot(command_prefix="!", intents=intents)

#-----The bot sends messages/respones through this function------#
async def send_message(message: Message,user_message: str) -> None:
    if not user_message:                      
        print('(Message was empty)')
        return
    
    if is_private := user_message[0] == '?':    # To check if the user wants a private reply
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)

@client.event 
async def on_ready() -> None:
    print(f'{client.user} is now runnning')

@client.event
async def on_voice_state_update(member, before, after):
    voice_client = discord.utils.get(client.voice_clients, guild=member.guild)
    if before.channel is None and after.channel is not None:
        voice_channel = after.channel

        if len(song_q) == 0:
            text_to_speech(f'Welcome {member.display_name}')  # Save the TTS to an audio file (speech.mp3)
            audio_source = FFmpegPCMAudio('speech.mp3')
            await asyncio.sleep(3)
            voice_client.play(audio_source)

        while voice_client.is_playing():
            await asyncio.sleep(1)

    
@client.event
async def on_message(message: Message):
    if message.author == client.user or message.author.bot:
        return

    if message.channel.id in allowed_channel_id:
        
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.content)

        if message.content.startswith("!remindme"):
            await cmnds(message)

        if message.content.startswith('!join'):
            await join_channel(message)

        if message.content.startswith('!leave'):
            await leave_channel(message)

        if message.content.startswith('!speak'):
            await speak_message(message)

        if message.content.startswith('!play'):
            query = message.content[len('!play '):]
            await play_song(message, query)             

        if message.content.startswith('!pause'):
            await pause_song(message)

        if message.content.startswith('!resume'):
            await resume_song(message)


        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message)
      
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()