import discord
from discord.ext import commands
import youtube_dl
import os
import time
import random
from dotenv import load_dotenv

# load environment variables and define
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

client = commands.Bot(command_prefix="!lofi ")


def isInt(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


lofiVideos = ["https://www.youtube.com/watch?v=5p7kA6xGSKo", "https://www.youtube.com/watch?v=p1Co7ANo6vs",
              "https://www.youtube.com/watch?v=lTRiuFIWV54", "https://www.youtube.com/watch?v=GA9GigGuf24", "https://www.youtube.com/watch?v=Xc1Le3CSdrM"]
rainVideos = ["https://www.youtube.com/watch?v=q76bMs-NwRk&t=11s", "https://www.youtube.com/watch?v=pO2_D2iDz30",
              "https://www.youtube.com/watch?v=_x3hVRSIe2g", "https://www.youtube.com/watch?v=M9JCzXtB2_w"]


lofiInit = ["Lofi Engaged 🎶", "It's time to chill 🎶", "Lofi Loading... 🎶"]
studyInit = ["Starting a session", "Good luck! Studying ", "Let's study"]
studyEnd = ["Time's up! well done!",
            "Let's take a break.", "Good job! You studied well"]

helpList = ["```✨Commands✨\n\n1. !lofi play           🎶 Embark on a lofi stroll - beats to relax/discord to.\n2. !lofi leave          ⛔ Disconnect the lofi bot.\n3. !lofi pause          ⏸️ Pause the lofi bot.\n4. !lofi resume         ▶️ Resume the lofi bot.\n5. !lofi stop           🛑 Stop the lofi currently playing.\n6. !lofi study {mins}   📚 Study with lofi for a set number of minutes.\n7. !lofi pom {cycles}   ⏱️ Study for a set number of pommodoro intervals!\n8. !lofi rain           ⛈️ Play comforting rain/thunder sounds.\n\nFor more information on each command, use !lofi info {command}```",
            "```!lofi play - Plays the lofi music bot indefinitely - ideal for chilling/studying for an unspecified amount of time.```",
            "```!lofi leave -  Disconnects the lofi bot regardless of what it's doing at the time - chill vibes over.```",
            "```!lofi pause - Pauses the lofi bot regardless of what it's doing at the time: vibes on hold.```",
            "```!lofi resume - Re-enable chill vibes, the lofi bot will continue streaming.```",
            "```!lofi stop = Stop the bot,```",
            "```!lofi study [minutes] - Begins a lofi study session for the amount of time specified. The bot will join and play lofi, and you will be notified when the time limit is up. The bot will also disconnect.```",
            "```!lofi pom [intervals] - Begins a lofi study session that follows the pommodoro technique for the number of intervals specified. You can set the number of intervals over which the bot will join and play lofi, notify you how long to take a break for between each study interval, then repeat the cycle for the amount of time specified. You can read more about the pommodoro technique here: https://en.wikipedia.org/wiki/Pomodoro_Technique```",
            "```!lofi rain - Play relaxing rain sounds on the lofi bot, perfect for studying, or some background noise.```"]


@client.event
async def on_ready():
    print(f'⚡ {client.user} has successfully connected to Discord! ⚡')

    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )


@client.command()
async def info(ctx, arg1=None):
    if arg1 == None:
        await ctx.send(helpList[0])

    elif arg1 == "play":
        await ctx.send(helpList[1])

    elif arg1 == "leave":
        await ctx.send(helpList[2])

    elif arg1 == "pause":
        await ctx.send(helpList[3])

    elif arg1 == "resume":
        await ctx.send(helpList[4])

    elif arg1 == "stop":
        await ctx.send(helpList[5])

    elif arg1 == "study":
        await ctx.send(helpList[6])

    elif arg1 == "pom":
        await ctx.send(helpList[7])

    elif arg1 == "rain":
        await ctx.send(helpList[8])

    else:
        await ctx.send("Please choose one of the commands listed by the `!lofi help` command, and try again.")
        # Study functionality


@client.command()
async def play(ctx):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await ctx.send(random.choice(lofiInit))
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([random.choice(lofiVideos)])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=GUILD)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=GUILD)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=GUILD)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=GUILD)
    voice.stop()


@client.command()
async def study(ctx, arg1):
    if arg1 == None:
        await ctx.send("Please specify the amount of time you would like to study for\n e.g. `!lofi study 15`")
        return
    elif isInt(arg1):
        x = 0

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        voiceChannel = discord.utils.get(
            ctx.guild.voice_channels, name='General')
        await ctx.send(random.choice(lofiInit))
        await voiceChannel.connect()
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([random.choice(lofiVideos)])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

        while x < (int(arg1)*60):
            time.sleep(1)
            x += 1
        await ctx.send(f"Session ended")
        if voice.is_connected():
            await voice.disconnect()
    else:
        await ctx.send("Please enter a number, and try again")
        return


@client.command()
async def pom(ctx, arg1=None):
    if arg1 == None:
        await ctx.send("Please specify the number of cycles you would like to study for\n e.g. `!lofi pom 3`")
        return

    elif isInt(arg1):
        i = 0
        pommodoroCycle = [25, 5, 25, 5, 25, 5, 25, 15]

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([random.choice(lofiVideos)])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")

        while i < arg1:
            for x in pommodoroCycle:
                if (x+1) % 2 != 0:
                    print("time to study for 25 minutes!")
                else:
                    if x == 7:
                        print("take a longer 15 minute break this time!")
                    else:
                        print("take a short 5 minute break.")

                executionTime = pommodoroCycle[x]*60

                voiceChannel = discord.utils.get(
                    ctx.guild.voice_channels, name='General')
                await ctx.send(random.choice(lofiInit))
                await voiceChannel.connect()
                voice = discord.utils.get(
                    client.voice_clients, guild=ctx.guild)

                voice.play(discord.FFmpegPCMAudio("song.mp3"))

                time.sleep(executionTime)

                # Alert the user and disconnect the voice client if it's still there
                if voice.is_connected():
                    await voice.disconnect()
                i += 1

    else:
        await ctx.send("Please enter a number, and try again")
        return

    print("Pommodoro session loading...")
    await ctx.send("Pommodoro session set")


@client.command()
async def rain(ctx):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await ctx.send(random.choice(lofiInit))
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([random.choice(rainVideos)])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))

client.run(TOKEN)
