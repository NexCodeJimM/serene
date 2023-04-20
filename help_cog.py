import nextcord
from nextcord.ext import commands


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Music commands:
s.shelp - displays all the available commands
s.p <keywords> - finds the song on youtube and plays it in your current channel. Will resume playing the current song if it was paused
s.q - displays the current music queue
s.skip - skips the current song being played
s.clear - Stops the music and clears the queue
s.leave - Disconnected the bot from the voice channel
s.pause - pauses the current song being played or resumes if already paused
s.resume - resumes playing the current song
```
"""
        self.text_channel_list = []

    # Some debug info so that we know the bot has started
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)

    @commands.command(name="shelp", help="Displays all the available commands")
    async def help_command(self, ctx):
        await ctx.send(embed=self.get_help_embed())

    def get_help_embed(self):
        embed = nextcord.Embed(title="Serene Available Commands",
                               description=self.help_message, color=0x00ff00)
        return embed

    async def send_to_all(self):
        for text_channel in self.text_channel_list:
            await text_channel.send(embed=self.get_help_embed())
