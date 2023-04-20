import nextcord
from nextcord.ext import commands


class moderation_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_message = nextcord.Embed(
            title="Warning", description="Please refrain from using bad language.", color=nextcord.Color.red())
        self.bad_words = set()

        # Load the bad words from the .txt file
        with open('bad_words.txt', 'r') as f:
            for line in f:
                self.bad_words.add(line.strip())

    # Listens to bad words in chat
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith(self.bot.command_prefix):
            return

        content = message.content.lower()
        for bad_word in self.bad_words:
            if bad_word in content:
                await message.delete()
                self.warn_message.set_author(
                    name=message.author.name, icon_url=message.author.avatar.url)
                await message.channel.send(embed=self.warn_message)
                break

    # Add bad words to .txt file via command
    @commands.command(name="badword", help="Adds a word to the list of bad words")
    async def add_bad_word(self, ctx, word):
        with open('bad_words.txt', 'a') as f:
            f.write(f"{word}\n")
        self.bad_words.add(word.lower())  # Add the new word to the set
        confirmation_message = nextcord.Embed(
            title="Bad Word Added", description=f"`{word}` has been added to the list of bad words.", color=nextcord.Color.green())
        await ctx.send(embed=confirmation_message)
