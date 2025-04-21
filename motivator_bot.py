import discord
from discord.ext import tasks, commands
import datetime
import random
import os
import json

# Safely load curated quotes from quotes.json
try:
    with open("quotes.json", "r", encoding="utf-8") as f:
        quotes = json.load(f)
    print(f"✅ Loaded {len(quotes)} quotes.")
except Exception as e:
    print(f"❌ Failed to load quotes.json: {e}")
    quotes = [{"text": "Default quote while loading failed.", "author": "System"}]

# Get environment variables from Railway
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# When the bot is ready
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    send_quote.start()

# Daily quote post at 8 AM (UTC time)
@tasks.loop(time=datetime.time(hour=8, minute=0))
async def send_quote():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        quote = random.choice(quotes)
        await channel.send(f"🌟 **Daily Motivation** 🌟\n> *{quote['text']}*\n\n— **{quote['author']}**")
    else:
        print(f"⚠️ Channel with ID {CHANNEL_ID} not found.")

# Run the bot
bot.run(TOKEN)



