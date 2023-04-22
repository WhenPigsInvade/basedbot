import discord
from discord.ext import commands

async def respond(message, words):
    for word in words:
        if message.content.__contains__(word):
            increment_value = f"""UPDATE guild_{message.guild.id} SET {word} = {val[word] + 1} WHERE uid = {message.author.id};"""
            cursor.execute(increment_value)
            conn.commit() # Commit once after every increment otherwise rollback will affect all previous incrementations.
        
    if message.content.__contains__("@everyone"):
        name = ["dipshit", "dumbass", "asshat"]
        await message.reply(f"Hey {random.choice(name)} we're trying to sleep over here.")    

    elif message.content.lower().__contains__("brb"):
        await message.channel.send("brb, on my way to fuck your mother.")