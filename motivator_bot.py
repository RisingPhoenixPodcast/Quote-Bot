import discord
from discord.ext import tasks, commands
import datetime
from datetime import timezone, timedelta
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

# Define the Eastern Time function
def get_eastern_time():
    # Check if we're in Daylight Saving Time
    now = datetime.datetime.now()
    is_dst = now.astimezone().dst() != timedelta(0)
    
    if is_dst:
        # Eastern Daylight Time (UTC-4)
        return datetime.time(hour=12, minute=0)  # 8 AM EDT = 12 PM UTC
    else:
        # Eastern Standard Time (UTC-5)
        return datetime.time(hour=13, minute=0)  # 8 AM EST = 13 PM UTC

# When the bot is ready
@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")
    send_quote.start()

# Daily quote post at 8 AM (Eastern time)
@tasks.loop(time=get_eastern_time())
async def send_quote():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        quote = random.choice(quotes)
        await channel.send(f"🌟 **Daily Motivation** 🌟\n> *{quote['text']}*\n\n— **{quote['author']}**")
    else:
        print(f"⚠️ Channel with ID {CHANNEL_ID} not found.")

# Run the bot
bot.run(TOKEN)



