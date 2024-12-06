import vlc
import discord
import yt_dlp
import asyncio
import os
import json
import subprocess
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True

prefix = '-'

bot = commands.Bot(command_prefix=prefix, intents=intents)
songs = asyncio.Queue()

# runs when bot is ready
@bot.event
async def on_ready():
    # await bot.load_extension('./cogs/music_cog.py')
    # for filename in os.listdir('./cogs'):
    #     if filename.endswith('.py'):
    #         await bot.load_extension(f'cogs.{filename[:-3]}')
    pass


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
    ffmpeg_options = {'options': '-vn'}
    pwd = repr(subprocess.check_output(["pwd"]))[1:-1]
    pwd = pwd[1:-2]
    

    song_id = song_info["id"]

    for fname in os.listdir("./"):
        if song_id in fname:
            await songs.put(fname)
            
    try:
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(await songs.get(), **ffmpeg_options))
    except discord.ClientException:
        ctx.send("deu uma bosta aqui")

@bot.event
async def audio_state(ctx):
    ffmpeg_options = {'options': '-vn'}

    while True:
        if not ctx.voice_client.is_playing():
            ctx.voice_client.play(discord.FFmpegPCMAudio(await songs.get(), **ffmpeg_options))
        await asyncio.sleep(3)

@bot.command()
async def stop(ctx):
    ctx.voice_client.stop()
    # ctx.voice_client.server.disc
    while not songs.empty():
        songs.get_nowait()
        songs.task_done()

@bot.command()
async def skip(ctx):
    ffmpeg_options = {'options': '-vn'}

    ctx.voice_client.stop()
    ctx.voice_client.play(discord.FFmpegPCMAudio(await songs.get(), **ffmpeg_options))

bot.run(os.environ.get("BOT_TOKEN"))

# song_info["requested_downloads"][0]["filepath"]
#pwd+"/"+song_info["title"]+".m4a"