# TODO: add placeholders to avoid SQL Injections in add()
import urllib.request
import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='$')
conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("F in chat for BasedBot 1.0"))
    print('bot online')
    print(bot.user.name)

@bot.command()
async def add(message, arg):

    if(arg is None):
        await message.channel.send("Invalid argument")
        return

    if(arg not in await fetch_columns(message)):
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


# Checks if guild exists in database, then checks if user exists.
async def exists(message):
    #Checks if guild exists in database or not, adds if necessary
    if cursor.execute(f"""SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='guild_{message.guild.id}');""").fetchall() == [(0,)]:
        print("Guild table not found, creating")
        cursor.execute(f"""CREATE TABLE guild_{message.guild.id} (uid INTEGER PRIMARY KEY);""")

    #Check if user is in database, adds if necessary
    if cursor.execute(f"""SELECT EXISTS (SELECT uid FROM guild_{message.guild.id} WHERE uid='{message.author.id}');""").fetchall() == [(0,)]:
        print("User not found in guild table. Adding to database")
        cursor.execute(f"""INSERT INTO guild_{message.guild.id} (uid) VALUES ({message.author.id});""")

    return


@bot.event
async def on_message(message):
    await exists(message)
        

    #Grab the list of words being tracked.


        

    conn.commit()
    await bot.process_commands(message)


# Runs the bot with the bot token from token.txt
with open("token.txt", "r") as file:
    token = file.read().splitlines()[0].strip()
bot.run(token)
