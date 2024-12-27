import yt_dlp
import discord

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}

def search_youtube(query):
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        except Exception as e:
            print(f"Error: {e}")
            return None
        return {'url':info['url'], 'title':info['title']}