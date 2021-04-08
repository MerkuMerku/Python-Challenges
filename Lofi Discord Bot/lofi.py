import os
import time
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables and define
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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

lofi_init = ["Lofi Engaged!", "It's time to chill!", "Lofi Loading..."]
session_init = ["Starting a session", "Good luck! Studying ", "Let's study"]
session_end = ["Time's up! well done!",
               "Let's take a break.", "Good job! You studied well"]

# strings for the help command
helplist = ["```Commands\n1. !lofi       Play lofi hiphop - beats to relax/discord to\n2. !lofi dc    Disconnect the lofi bot\n3. !lofi study Study with lofi for a set number of minutes\n4. !lofi pom   Study to a set number of pommodoro intervals!```",
            "```!lofi Plays the lofi music bot indefinitely - ideal for chilling/studying for an unspecified amount of time.```",
            "```!lofi dc disconnects the lofi bot regardless of what it's doing at the time - chill vibes over.```",
            "```!lofi study [minutes] begins a lofi study session for the amount of time specified. The bot will join and play lofi, and you will be notified when the time limit is up. The bot will also disconnect.```",
            "```!lofi pom [intervals] begins a lofi study session that follows the pommodoro technique for the number of intervals specified. You can set the number of intervals over which the bot will join and play lofi, notify you how long to take a break for between each study interval, then repeat the cycle for the amount of time specified. You can read more about the pommodoro technique here: https://en.wikipedia.org/wiki/Pomodoro_Technique```"]

# function for checking if a string can be converted to an int


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


def pommodoro(val)


@client.command()
async def lofi(ctx, arg1=None, arg2=None):

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if arg1 == None:
        print("Lofi loading...")
        await ctx.send(random.choice(lofi_init))
        # set up voice client
        await voiceChannel.connect()

    elif arg1 == "dc":
        if not voice.is_connected():
            return
        else:
            await voice.disconnect()

    elif arg1 == "help":
        if arg2 == None:
            await ctx.send(helplist[0])

        elif arg2 == "!lofi":
            await ctx.send(helplist[1])

        elif arg2 == "!lofi dc":
            await ctx.send(helplist[2])

        elif arg2 == "!lofi study":
            await ctx.send(helplist[3])

        elif arg2 == "!lofi pom":
            await ctx.send(helplist[4])

        else:
            await ctx.send("Please choose one of the commands listed by the `!lofi help` command, and try again.")
            # Study functionality

    elif arg1 == "study":
        if arg2 == None:
            await ctx.send("Please specify the amount of time you would like to study for\n e.g. `!lofi study 15`")
            return

        elif is_int(arg2):
            # Calculate the number of seconds to stay active
            entered_time = round(int(arg2)*60)

            # Alert the users that the session has begun for the selected time
            await ctx.send(f"{random.choice(session_init)} for {arg2} minutes 🧠⚡")

            # Sleep function for the set time
            time.sleep(entered_time)
            await ctx.send(f"Session ended - {random.choice(session_end)}")
            # Disconnect the voice client if it's still there
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

        elif is_int(arg2):
            # Calculate the number of seconds to stay active
            entered_time = round(int(arg2)*60)

            # Alert the users that the session has begun for the selected time
            await ctx.send(f"{random.choice(session_init)} for {arg2} minutes")

            # Sleep function for the set time
            time.sleep(entered_time)
            await ctx.send(f"Session ended - {random.choice(session_end)}")
            # Disconnect the voice client if it's still there
            if voice.is_connected():
                await voice.disconnect()
        else:
            await ctx.send("Please enter a number, and try again")
            return

        print("Pommodoro session loading...")
        await ctx.send("Pommodoro session set")

    else:
        await ctx.send("I don't recognise this command - for help using the Lofi Study Bot, use `!study help`")
        return

client.run(TOKEN)
