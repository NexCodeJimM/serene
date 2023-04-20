import nextcord
from nextcord.ext import commands
import os

from dotenv import load_dotenv

from help_cog import help_cog
from music_cog import music_cog
from moderation_cog import moderation_cog

load_dotenv()

intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='s.', intents=intents)

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))
bot.add_cog(moderation_cog(bot))


@bot.event
async def on_ready():
    # Show console log when bot is online
    print("Serene is now Online!")
    # Bot Activity Status
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Under Development"))


bot.run(os.environ.get("TOKEN"))
