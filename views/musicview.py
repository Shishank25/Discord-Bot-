import discord
import asyncio

class MusicView(discord.ui.View):

    def __init__(self, guild, message, song_q):
        self.guild = guild
        self.message = message
        self.song_q = song_q
        self.voice_client = self.message.guild.voice_client
        super().__init__()
        print('class works!')


    @discord.ui.button(label='Stop', style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # voice_client = self.message.guild.voice_client
        guild_id = interaction.guild.id
        if self.voice_client:
            self.voice_client.stop()
            self.song_q[guild_id] = []
            await interaction.response.send_message("Playback Stopped.", ephemeral=True)
            self.resume_button.disabled = self.pause_button.disabled = self.stop_button.disabled = True
            await interaction.message.edit(view=self)
            await asyncio.sleep(3)
            await interaction.message.delete()
        else:
            await interaction.response.send_message("No audio is currently playing.", ephemeral=True)  
        

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # voice_client = self.message.guild.voice_client
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.pause_button.disabled = True
            self.resume_button.disabled = False
            await interaction.message.edit(view=self)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("No audio is currently playing.", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.secondary)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # voice_client = self.message.guild.voice_client
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            self.pause_button.disabled = False
            self.resume_button.disabled = True
            await interaction.message.edit(view=self)
            await interaction.response.defer()
        else:
            await interaction.response.send_message("No audio is currently paused.", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.green)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # voice_client = self.message.guild.voice_client
        if self.voice_client:
            self.voice_client.stop()
            await interaction.response.send_message('Next!', ephemeral=True)
            await asyncio.sleep(2)
            await interaction.message.delete()

    @discord.ui.button(label='Queue', style=discord.ButtonStyle.secondary)
    async def queue_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        guild_id = interaction.guild.id

        if guild_id in self.song_q and self.song_q[guild_id]:
            queue_list = self.song_q[guild_id]

            queue_message = '\n'.join([f'{index + 1}. {song['title']}' for index,song in enumerate(queue_list)])
            await interaction.response.send_message(f'Current queue:\n{queue_message}',ephemeral=True)

        else:
            await interaction.response.send_message("The queue is empty.", ephemeral=True)
