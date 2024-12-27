from discord import Client, Message, FFmpegPCMAudio
from commands.music import play_song, pause_song, resume_song
from utils.utils import text_to_speech, parse_time
from utils.response import get_response, get_response1
import asyncio

async def cmnds(message: Message):
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.content)
    try:
        # Use `get_response` to parse the message and extract the time and reminder
        response_data = get_response1(message.content)
        # Assuming `get_response` returns a dict with 'time' and 'message'
        time_str = response_data['time']
        reminder_msg = response_data['message']

        # Convert the time string to seconds
        reminder_time = parse_time(time_str)
        
        if reminder_time is None:
            await message.channel.send("Invalid time format. Use 's', 'm', or 'h'.")
            return

        # Send confirmation to the user
        await message.channel.send(f"Reminder set! I will remind you in {time_str}: {reminder_msg}")

        # Wait for the specified amount of time
        await asyncio.sleep(reminder_time)

        # Send the reminder
        await message.channel.send(f"⏰ Reminder: {reminder_msg}, {message.author.mention}!")

        text_to_speech(reminder_msg)
        audio_source = FFmpegPCMAudio('speech.mp3')

        # Check if the user is in a voice channel
        
        if message.author.voice:  # Check if the author is in a voice channel
            channel = message.author.voice.channel  # Get the voice channel object
    
            # Check if the bot is already connected to a voice channel
            if message.guild.voice_client:
                # If already connected, play the audio
                voice_client = message.guild.voice_client
                if not voice_client.is_playing():
                    voice_client.play(audio_source)
            else:
                # If not connected, connect to the user's voice channel
                voice_client = await channel.connect()
                voice_client.play(audio_source)

            # Wait asynchronously until the audio is finished playing
            while voice_client.is_playing():
                await asyncio.sleep(1)  # This keeps the bot from blocking other tasks

            # Disconnect after playing the audio
            await voice_client.disconnect()

        else:
            await message.channel.send(f"⏰ Reminder: {reminder_msg}, {message.author.mention}!")
        
    except KeyError:
        await message.channel.send("Error: Unable to parse the message. Please use the correct format: `!remindme <time> <message>`")
    except Exception as e:
        await message.channel.send(f"An error occurred: {str(e)}, Reminder Format is '!remindme <time> <message>'")

async def join_channel(message: Message):
    # Get the user's voice channel
    if message.author.voice:
        channel = message.author.voice.channel
        # If the bot is not already in a voice channel
        if not message.guild.voice_client:
            voice_client = await channel.connect()  # Join the voice channel
            print(f'voice_client for join: {voice_client}')
            await message.channel.send(f"Joined {channel}")
        else:
            await message.channel.send("I'm already connected to a voice channel!")
    else:
        await message.channel.send("You are not in a voice channel.")

async def leave_channel(message: Message):
    # If the bot is in a voice channel
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()  # Leave the voice channel
        await message.channel.send("Disconnected from the voice channel.")
    else:
        await message.channel.send("I'm not in a voice channel.")

async def speak_message(message: Message):
    # Ensure the user is in a voice channel
    if message.author.voice:
        channel = message.author.voice.channel

        # Text to speech conversion
        text_to_speak = message.content[len('!speak '):]  # Get the message after the !speak command
        text_to_speech(text_to_speak)  # Save the TTS to an audio file (speech.mp3)

        # Play the generated speech
        audio_source = FFmpegPCMAudio('speech.mp3')

        if message.guild.voice_client:                    
            message.guild.voice_client.play(audio_source)
        elif not message.guild.voice_client:
            voice_client = await channel.connect()
            voice_client.play(audio_source)

        # Wait for the audio to finish playing
        while message.guild.voice_client.is_playing():
            await asyncio.sleep(1)