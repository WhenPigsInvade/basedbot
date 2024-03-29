# TODO add placeholders to avoid SQL Injections in add()
# TODO merge fetch_column(message) command with column_exists(message, arg) --- So it returns simple true or false
# TODO split functions up into individual modules
import urllib.request # Depreciated
import discord
from discord.ext import commands
import random # random quote selection
import sqlite3 # for database
import time
import os
import asyncio

# Import basedbot modules
import responses

# For some reason master sqlite table is sqlite_master on Linux
master_table = "sqlite_schema"
if os.name == "posix":
    master_table = "sqlite_master"

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=discord.Intents.all())
conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

with open('quotes.txt') as f:
    quotes = [line.rstrip() for line in f]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("You can now mention me to use commands!"))
    print('bot online')
    print(bot.user.name)

@bot.command()
async def add(message, arg):

    if(arg is None):
        await message.channel.send("Invalid argument")
        return

    if(arg in await fetch_columns(message)):
        await message.channel.send("Keyword is already being logged.")
        return

    try:
        # Make sure guild is in database.
        await exists(message)

        # REMINDER: use placeholders to avoid SQL injections!!! https://docs.python.org/3/library/sqlite3.html
        alter_query = f"""ALTER TABLE guild_{message.guild.id} ADD COLUMN {arg} NOT NULL DEFAULT 0;"""


        await message.channel.send(f"{arg} is now logged on this server.")
        cursor.execute(alter_query)
        conn.commit()
    
    except:
        await message.channel.send("Error. Please try again.")

@bot.command()
async def remove(message, arg):

    # Don't let the user drop the uid column!
    if(arg is None or arg == "uid"):
        await message.channel.send("Invalid argument")
        return

    if(arg not in await fetch_columns(message)):
        await message.channel.send("Keyword is not being logged.")
        return

    try:
        # Make sure guild is in database.
        await exists(message)

        # REMINDER: use placeholders to avoid SQL injections!!! https://docs.python.org/3/library/sqlite3.html
        alter_query = f"""ALTER TABLE guild_{message.guild.id} DROP COLUMN {arg};"""


        await message.channel.send(f"{arg} is no longer logged on this server.")
        cursor.execute(alter_query)
        conn.commit()
    
    except:
        await message.channel.send("Error. Please try again.")

# Grabs the list of words being tracked
async def fetch_columns(message):
    fetch_columns = f"""PRAGMA table_info(guild_{message.guild.id});"""
    
    cursor.execute(fetch_columns)
    columns = []
    for item in cursor.fetchall():
        columns.append(item[1])

    return columns

# TODO merge command with column_exists(message, arg)
# Checks if guild exists in database, then checks if user exists.
async def exists(message):
    #Checks if guild exists in database or not, adds if necessary
    # Might be sqlite_schema or sqlite_master depending on sqlite version / platform
    if cursor.execute(f"""SELECT EXISTS (SELECT name FROM {master_table} WHERE type='table' AND name='guild_{message.guild.id}');""").fetchall() == [(0,)]:
        print("Guild table not found, creating")
        cursor.execute(f"""CREATE TABLE guild_{message.guild.id} (uid INTEGER PRIMARY KEY);""")

    #Check if user is in database, adds if necessary
    if cursor.execute(f"""SELECT EXISTS (SELECT uid FROM guild_{message.guild.id} WHERE uid='{message.author.id}');""").fetchall() == [(0,)]:
        print("User not found in guild table. Adding to database")
        cursor.execute(f"""INSERT INTO guild_{message.guild.id} (uid) VALUES ({message.author.id});""")

    conn.commit()
    return

@bot.command(name = 'top')
async def fetch_leaderboard(message, arg):

    if arg is None:
        await message.channel.send("Invalid parameter.")
        return

    # Checks keyword is being tracked
    if arg not in await fetch_columns(message):
        await message.channel.send("Keyword is not tracked right now.")
        return

    # Fetch list of top performers
    toppers = cursor.execute(f"""SELECT uid, {arg} FROM guild_{message.guild.id} ORDER BY {arg} DESC""").fetchall()

    # Only show top 10
    if toppers.__len__() > 10:
        toppers = toppers[:10]

    # Create embed
    embed=discord.Embed(title=f"{arg}", description=f"Top usage of {arg} \nRequested by {message.author.display_name}", color=discord.Color.red())

    # Add line breaker
    # embed.add_field(name = chr(173), value = chr(173), inline=False)

    for usr in toppers:
        if usr[1] != 0:
            # print(str(usr[0]) + " " + str(usr[1]))
            embed.add_field(name=f"{(await bot.fetch_user(usr[0])).display_name}", value=f"{usr[1]}", inline=False)
    
    embed.set_footer(text=f"{random.choice(quotes)}")

    # embed.set_author(name=message.author.display_name, icon_url="https://i.imgur.com/4N9vIOM.jpeg")

    await message.send(embed=embed)

@bot.command(name = 'keywords')
async def fetch_keywords(message):
    keywords = (await fetch_columns(message))[1:]

    if keywords == []:
        message.channel.send("No keywords are being tracked on this server right now.")
        return

    # Create embed
    embed=discord.Embed(title=f"List of currently tracked keywords", description=f"Requested by {message.author.display_name}", color=discord.Color.red())

    for word in keywords:
        embed.add_field(name = f"{word}", value=f"\u200b", inline=False)
    
    embed.set_footer(text=f"{random.choice(quotes)}")

    await message.channel.send(embed=embed)

bot.remove_command("help") # NEED THIS LINE: There is already a built in "help" command
# to bots for some reason. Need to remove it for our custom one to work
@bot.command(name="help")
async def show_commands(message):
    # Create embed
    embed=discord.Embed(title="Commands", description=f"List of commands \nRequested by {message.author.display_name}", color=discord.Color.red())


    embed.add_field(name = f"keywords\ntop [word]\nremove\nadd\nlog", value=f"\u200b", inline=False)
    
    embed.set_footer(text=f"{random.choice(quotes)}")

    # embed.set_author(name=message.author.display_name, icon_url="https://i.imgur.com/4N9vIOM.jpeg")

    await message.send(embed=embed)

@bot.command()
async def log(message):
    response = [
        "Ok, I'm in.", 
        "Nope. My log is too big :/"
    ]
    await message.send("Fitting my log in your ass")
    await asyncio.sleep(3)
    await message.send(random.choice(response))
  


@bot.event
async def on_message(message):

    # If user is bot
    if message.author.bot:
        return


    await exists(message)
        

    #Grab the list of words being tracked.
    words = await fetch_columns(message)
    words = words[1:] # Trims out uid

    # Fetches keyword count for current user
    fetch_value = f"""SELECT * FROM guild_{message.guild.id} WHERE uid = {message.author.id};"""
    values = cursor.execute(fetch_value).fetchone()
    values = values[1:] # Trims out uid

    val = dict(zip(words, values))

    # Checks of each keyword being logged is present inside sent message.
    # Responses for additional keyphrases, i.e. brb
    await responses.respond(message, words)

    # Required to keep the bot running after on_message()
    await bot.process_commands(message)


# Runs the bot with the bot token from token.txt
with open("token.txt", "r") as file:
    token = file.read().splitlines()[0].strip()
bot.run(token)
