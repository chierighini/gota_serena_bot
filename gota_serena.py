import vlc
import discord
import yt_dlp
import os
import subprocess
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True

prefix = '-'

bot = commands.Bot(command_prefix=prefix, intents=intents)

# runs when bot is ready
@bot.event
async def on_ready():
    # await bot.load_extension('./cogs/music_cog.py')
    # for filename in os.listdir('./cogs'):
    #     if filename.endswith('.py'):
    #         await bot.load_extension(f'cogs.{filename[:-3]}')
    pass


#plays music, but gets cut off by youtube (stream issue?)
@bot.command()
async def play(ctx, url):
    voiceChannel = ctx.message.author.voice.channel
    try:
        await voiceChannel.connect()
    except discord.ClientException:
        pass



    ydl_opts = {'format': 'bestaudio'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        song_info = ydl.extract_info(url, download=True)
    # with open("./queue_file","a") as queue_file:
    #     queue_file.write(song_info["title"])
    ffmpeg_options = {'options': '-vn'}
    pwd = repr(subprocess.check_output(["pwd"]))[1:-1]
    pwd = pwd[1:-2]

    title = song_info["title"]
    for fname in os.listdir("./"):
        if title in fname:
            path = fname

    ctx.voice_client.play(discord.FFmpegPCMAudio(path, **ffmpeg_options))

bot.run(os.environ.get("BOT_TOKEN"))


#pwd+"/"+song_info["title"]+".m4a"

# async def streamx(ctx, url):
#     voiceChannel = ctx.message.author.voice.channel #get Message Sender Channel. When you want it to join without a seperat function.
#     await voiceChannel.connect() #same applies to this
#     ffmpeg_options = {'options': '-vn'}
#     ydl_opts = {'format': 'bestaudio'}
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         song_info = ydl.extract_info(url, download=False)

#     ctx.voice_client.play(discord.FFmpegPCMAudio(song_info["url"], **ffmpeg_options))    



# def get_music_from_link(link):
#     # URLS = ['https://www.youtube.com/watch?v=dQw4w9WgXcQ']

#     ydl_opts = {
#         'format': 'm4a/bestaudio/best',
#         # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
#         'postprocessors': [{  # Extract audio using ffmpeg
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'm4a',
#         }]
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         error_code = ydl.download(link)


# def play_audio(stream):
#     i = vlc.Instance()


# # Instance = vlc.Instance()
# player = Instance.media_player_new()
# Media = Instance.media_new(playurl)
# Media.get_mrl()
# player.set_media(Media)
# player.play()
