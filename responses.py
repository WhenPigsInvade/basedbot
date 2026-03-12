import discord
import random

async def respond(message, words):
    # 1. Handle special triggers
    # Using 'in' is cleaner than '__contains__'
    if "@everyone" in message.content:
        names = ["dipshit", "dumbass", "asshat"]
        await message.reply(f"Hey {random.choice(names)}, we're trying to sleep over here.")    

    elif "brb" in message.content.lower():
        await message.channel.send("brb, on my way to fuck your mother.")

    elif message.content.lower().strip() == "f":
        await message.channel.send("F? F what? The letter before G? The letter after E? Did you know that in Fu the F stands for \"fuck?\" So your reply is 'fuck?' or F as in Flourine? F as in I can fuck you?")

    # NOTE: We removed the database UPDATE logic from here 
    # because it is now handled automatically in the main script's on_message.