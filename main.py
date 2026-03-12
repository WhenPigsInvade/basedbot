import discord
from discord.ext import commands
import random
import sqlite3
import os
import asyncio
import re
import responses

# --- Setup & Database ---
intents = discord.Intents.all()
intents.message_content = True  # Required for v2.0+ prefix commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), intents=intents)
bot.help_command = None  # Modern way to disable default help

conn = sqlite3.connect("userdata.db")
cursor = conn.cursor()

# OS-specific master table name
master_table = "sqlite_master" if os.name == "posix" else "sqlite_schema"

with open('quotes.txt') as f:
    quotes = [line.rstrip() for line in f]

def clean_name(name):
    """Helper to prevent SQL injection on table/column names."""
    return re.sub(r'\W+', '', name)

# --- Helper Functions ---

async def get_columns(guild_id):
    """Returns a list of tracked column names for a specific guild."""
    safe_table = f"guild_{guild_id}"
    cursor.execute(f"PRAGMA table_info({safe_table});")
    return [item[1] for item in cursor.fetchall()]

async def ensure_exists(ctx):
    """Ensures the guild table and the user row exist."""
    table_name = f"guild_{ctx.guild.id}"
    
    # Check for table
    cursor.execute(f"SELECT name FROM {master_table} WHERE type='table' AND name=?", (table_name,))
    if not cursor.fetchone():
        cursor.execute(f"CREATE TABLE {table_name} (uid INTEGER PRIMARY KEY);")

    # Check for user
    cursor.execute(f"SELECT uid FROM {table_name} WHERE uid=?", (ctx.author.id,))
    if not cursor.fetchone():
        cursor.execute(f"INSERT INTO {table_name} (uid) VALUES (?)", (ctx.author.id,))
    
    conn.commit()

# --- Commands ---

@bot.event
async def on_ready():
    activity = discord.Game("Mention me or use $")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

@bot.command()
async def add(ctx, keyword: str = None):
    if not keyword:
        return await ctx.send("Please provide a keyword to add.")

    keyword = clean_name(keyword)
    await ensure_exists(ctx)
    
    columns = await get_columns(ctx.guild.id)
    if keyword in columns:
        return await ctx.send(f"'{keyword}' is already being logged.")

    try:
        # Note: Column names can't be parameterized with ?, so we use our cleaner
        cursor.execute(f'ALTER TABLE guild_{ctx.guild.id} ADD COLUMN "{keyword}" INTEGER NOT NULL DEFAULT 0;')        
        conn.commit()
        await ctx.send(f"**{keyword}** is now being logged on this server.")
    except Exception as e:
        print(f"Error adding column: {e}")
        await ctx.send("An error occurred. Make sure the keyword is valid.")

@bot.command()
async def remove(ctx, keyword: str = None):
    if not keyword or keyword.lower() == "uid":
        return await ctx.send("Invalid argument.")

    keyword = clean_name(keyword)
    columns = await get_columns(ctx.guild.id)

    if keyword not in columns:
        return await ctx.send("That keyword is not being logged.")

    try:
        cursor.execute(f"ALTER TABLE guild_{ctx.guild.id} DROP COLUMN {keyword};")
        conn.commit()
        await ctx.send(f"Stopped logging **{keyword}**.")
    except Exception as e:
        print(f"Error dropping column: {e}")
        await ctx.send("Failed to remove keyword.")

@bot.command(name='top')
async def fetch_leaderboard(ctx, keyword: str = None):
    if not keyword:
        return await ctx.send("Please specify a keyword (e.g., `$top 67`).")

    keyword = clean_name(keyword)
    columns = await get_columns(ctx.guild.id)

    if keyword not in columns:
        return await ctx.send("That keyword is not tracked.")

    table = f"guild_{ctx.guild.id}"
    
    # WRAP KEYWORD IN DOUBLE QUOTES HERE:
    query = f'SELECT uid, "{keyword}" FROM {table} WHERE "{keyword}" > 0 ORDER BY "{keyword}" DESC LIMIT 10'
    
    try:
        cursor.execute(query)
        toppers = cursor.fetchall()

        embed = discord.Embed(
            title=f"Leaderboard: {keyword}", 
            description=f"Top usage in this server", 
            color=discord.Color.red()
        )

        for uid, count in toppers:
            # Using get_user first is faster; fetch_user makes an API call
            user = bot.get_user(uid) or await bot.fetch_user(uid)
            name = user.display_name if user else f"User {uid}"
            embed.add_field(name=name, value=str(count), inline=False)
        
        embed.set_footer(text=random.choice(quotes))
        await ctx.send(embed=embed)
    except Exception as e:
        print(f"Error fetching leaderboard: {e}")
        await ctx.send("An error occurred while fetching the leaderboard.")

@bot.command()
async def keywords(ctx):
    all_cols = await get_columns(ctx.guild.id)
    tracked = all_cols[1:] # Skip 'uid'

    if not tracked:
        return await ctx.send("No keywords are being tracked yet.")

    embed = discord.Embed(title="Tracked Keywords", color=discord.Color.red())
    embed.description = "\n".join([f"• {word}" for word in tracked])
    embed.set_footer(text=random.choice(quotes))
    await ctx.send(embed=embed)

@bot.command(name="help")
async def show_help(ctx):
    if random.random() > .80:
        embed = discord.Embed(title="Bot Commands", color=discord.Color.red())
        embed.add_field(
            name="Available Commands", 
            value="`add [word]` - Start tracking a word\n`remove [word]` - Stop tracking\n`keywords` - Show tracked words\n`top [word]` - Leaderboard\n`log` - Fun command", 
            inline=False
        )
        embed.set_footer(text=random.choice(quotes))
        await ctx.send(embed=embed)
    else:
        await ctx.send("Yup, you need help for sure...")

@bot.command()
async def log(ctx):
    responses_list = ["Ok, I'm in.", "Nope. My log is too big :/"]
    await ctx.send("Checking the log...")
    await asyncio.sleep(2)
    await ctx.send(random.choice(responses_list))

@bot.event
async def on_message(message):
    # 1. Ignore bots and DMs
    if message.author.bot or not message.guild:
        return

    # 2. Ensure user and guild exist in DB before we try to update them
    # We use the helper function from earlier
    await ensure_exists(ctx=await bot.get_context(message))

    # 3. Get the list of tracked keywords for this server
    tracked_words = await get_columns(message.guild.id)
    # Remove 'uid' from the list so we only check keywords
    keywords = [word for word in tracked_words if word != 'uid']

    # 4. Count occurrences of each keyword in the message
    # We use case-insensitive matching here
    content_lower = message.content.lower()
    
    updates = []
    for word in keywords:
        # Count how many times the keyword appears
        # .count() is simple; for complex regex matching, you'd use re.findall
        count = content_lower.count(word.lower())
        if count > 0:
            updates.append((word, count))

    # 5. Update the database if keywords were found
    if updates:
        table_name = f"guild_{message.guild.id}"
        for word, amount in updates:
            # We use double quotes around {word} again for numeric/reserved keywords
            query = f'UPDATE {table_name} SET "{word}" = "{word}" + ? WHERE uid = ?'
            cursor.execute(query, (amount, message.author.id))
        conn.commit()

    # 6. Run additional response logic from your external module
    # Note: passing keywords list as requested in your original code
    if hasattr(responses, 'respond'):
        await responses.respond(message, keywords)

    # 7. CRITICAL: Process commands
    # Without this, $top, $add, etc., will stop working
    await bot.process_commands(message)

# Run
with open("token.txt", "r") as file:
    token = file.read().strip()
bot.run(token)