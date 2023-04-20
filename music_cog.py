import nextcord
from nextcord.ext import commands

from pytube import YouTube


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'options': '-vn'}

        self.vc = None

    # Search Music from Youtube then return the entiries and url
    def search_yt(self, item):
        try:
            video = YouTube("https://www.youtube.com/watch?v=" + item)
        except Exception:
            return False

        return {'source': video.streams.filter(only_audio=True).first().url, 'title': video.title}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # Get the first URL
            m_url = self.music_queue[0][0]['source']

            # Remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # Check for infinite loop
    async def play_music(self, ctx):
        # If the bot is already playing music, just add the new song to the queue and return
        if self.is_playing:
            embed = discord.Embed(
                title="Song added to the queue.", color=0x00ff00)
            await ctx.send(embed=embed)
            self.music_queue.append(
                [self.search_yt(query), ctx.author.voice.channel])
            return

        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # Try to connect to voice channel if you are not already connected
            if self.vc == None:
                self.vc = await self.music_queue[0][1].connect()

                # In case we fail to connect
                if self.vc == None:
                    embed = discord.Embed(
                        title="Could not connect to the voice channel.", color=0xff0000)
                    await ctx.send(embed=embed)
                    return
            elif not self.vc.is_connected():
                await self.vc.move_to(self.music_queue[0][1])

            # Remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(nextcord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", aliases=["p", "playing"], help="Plays a selected song from Youtube.")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # You need to be connected to a voice channel so the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format, try a different keyword.")
            else:
                await ctx.send("Song added to the queue.")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song being played.")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="resume", aliases=["r"], help="Resumes playing the current song being played.")
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played.")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            # Try to play the next song in the queue if it exists
            await self.play_music(ctx)

    @commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue.")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # Display a max of 5 songs in the queue
            if (i > 4):
                break
            retval += self.music_queue[i][0]['title'] + "\n"

            if retval != "":
                await ctx.send(retval)
            else:
                await ctx.send("No music in queue.")

    @commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue.")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared.")

    @commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
    async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
