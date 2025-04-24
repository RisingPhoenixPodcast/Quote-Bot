import discord
from discord.ext import tasks, commands
import datetime
from datetime import timezone, timedelta
import random
import os
import json

# Get the absolute path for quotes.json
script_dir = os.path.dirname(os.path.abspath(__file__))
quotes_path = os.path.join(script_dir, "quotes.json")

# Safely load curated quotes from quotes.json
try:
    with open(quotes_path, "r", encoding="utf-8") as f:
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
    try:
        print(f"🤖 Logged in as {bot.user}")
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print(f"⚠️ WARNING: Channel {CHANNEL_ID} not found at startup!")
        else:
            print(f"✅ Channel found: #{channel.name}")
        send_quote.start()
    except Exception as e:
        print(f"❌ Error in on_ready: {e}")

# Daily quote post at 8 AM (Eastern time)
@tasks.loop(time=get_eastern_time())
async def send_quote():
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            quote = random.choice(quotes)
            await channel.send(f"🌟 **Daily Motivation** 🌟\n> *{quote['text']}*\n\n— **{quote['author']}**")
            print(f"✅ Quote sent successfully at {datetime.datetime.now()}")
        else:
            print(f"⚠️ Channel with ID {CHANNEL_ID} not found.")
    except Exception as e:
        print(f"❌ Error sending quote: {e}")

# Test command to check if quotes are working
@bot.command()
async def testquote(ctx):
    try:
        quote = random.choice(quotes)
        await ctx.send(f"🌟 **Test Motivation** 🌟\n> *{quote['text']}*\n\n— **{quote['author']}**")
        await ctx.send("✅ Quote system is working!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# Test command to check channel access
@bot.command()
async def testchannel(ctx):
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("🔍 Channel access test - Bot is working!")
            await ctx.send(f"✅ Successfully sent message to <#{CHANNEL_ID}>")
        else:
            await ctx.send(f"❌ Could not find channel with ID {CHANNEL_ID}")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

# Run the bot
bot.run(TOKEN)



