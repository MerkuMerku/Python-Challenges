import os
import time
import random
import discord
import threading
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables and define
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('DISCORD_CHANNEL')

# set the client & command prefix
client = commands.Bot(command_prefix="!")

# test connection to guild


@client.event
async def on_ready():
    print(f'⚡ {client.user} has successfully connected to Discord! ⚡')

    # list connected guilds & members - not strictly production code
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

lofiInit = ["Lofi Engaged!", "It's time to chill!", "Lofi Loading..."]
sessionInit = ["Starting a session", "Good luck! Studying ", "Let's study"]
sessionEnd = ["Time's up! well done!",
              "Let's take a break.", "Good job! You studied well"]

# strings for the help command
helpList = ["```Commands\n1. !lofi       Play lofi hiphop - beats to relax/discord to\n2. !lofi dc    Disconnect the lofi bot\n3. !lofi study Study with lofi for a set number of minutes\n4. !lofi pom   Study for a set number of pommodoro intervals!```",
            "```!lofi Plays the lofi music bot indefinitely - ideal for chilling/studying for an unspecified amount of time.```",
            "```!lofi dc disconnects the lofi bot regardless of what it's doing at the time - chill vibes over.```",
            "```!lofi study [minutes] begins a lofi study session for the amount of time specified. The bot will join and play lofi, and you will be notified when the time limit is up. The bot will also disconnect.```",
            "```!lofi pom [intervals] begins a lofi study session that follows the pommodoro technique for the number of intervals specified. You can set the number of intervals over which the bot will join and play lofi, notify you how long to take a break for between each study interval, then repeat the cycle for the amount of time specified. You can read more about the pommodoro technique here: https://en.wikipedia.org/wiki/Pomodoro_Technique```"]

# function for checking if a string can be converted to an int


def isInt(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


@client.command()
async def lofi(ctx, arg1=None, arg2=None):

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if arg1 == None:
        await ctx.send(random.choice(lofiInit))
        await voiceChannel.connect()
        print("test")

    elif arg1 == "dc":
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The lofi bot is not currently connected")

    elif arg1 == "help":
        if arg2 == None:
            await ctx.send(helpList[0])

        elif arg2 == "!lofi":
            await ctx.send(helpList[1])

        elif arg2 == "dc":
            await ctx.send(helpList[2])

        elif arg2 == "study":
            await ctx.send(helpList[3])

        elif arg2 == "pom":
            await ctx.send(helpList[4])

        else:
            await ctx.send("Please choose one of the commands listed by the `!lofi help` command, and try again.")
            # Study functionality

    elif arg1 == "study":
        if arg2 == None:
            await ctx.send("Please specify the amount of time you would like to study for\n e.g. `!lofi study 15`")
            return

        elif isInt(arg2):
            voiceChannel = discord.utils.get(
                ctx.guild.voice_channels, name='General')
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

            # Connect and wait for the time period specified
            await voiceChannel.connect()
            time.sleep(int(arg2)*60)
            if time

            # Alert the user and disconnect the voice client if it's still there
            await ctx.send(f"Session ended")
            if voice.is_connected():
                await voice.disconnect()

        else:
            await ctx.send("Please enter a number, and try again")
            return

    # Pommodoro functionality
    elif arg1 == "pom":
        if arg2 == None:
            await ctx.send("Please specify the number of cycles you would like to study for\n e.g. `!lofi pom 3`")
            return

        elif isInt(arg2):
            i = 0
            pommodoroCycle = [25, 5, 25, 5, 25, 5, 25, 15]
            while i < arg2:
                for x in pommodoroCycle:
                    if (x+1) % 2 != 0:
                        print("time to study for 25 minutes!")
                    else:
                        if x == 7:
                            print("take a longer 15 minute break this time!")
                        else:
                            print("take a short 5 minute break.")

                    # run the timed connection function
                    executionTime = pommodoroCycle[x]*60
                    voiceChannel = discord.utils.get(
                        ctx.guild.voice_channels, name='General')
                    voice = discord.utils.get(
                        client.voice_clients, guild=ctx.guild)

                    # Connect and wait for the time period specified
                    await voiceChannel.connect()
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

    else:
        await ctx.send("I don't recognise this command - for help using the Lofi Study Bot, use `!study help`")
        return

client.run(TOKEN)
