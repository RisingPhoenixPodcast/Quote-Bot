import discord
from discord.ext import tasks, commands
import requests
import datetime
import os

TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    send_quote.start()

@tasks.loop(time=datetime.time(hour=8, minute=0))  # 8 AM daily
async def send_quote():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            await channel.send(f"🌟 **Daily Motivation** 🌟\n> *{quote}*\n\n— **{author}**")
        except Exception as e:
            await channel.send("⚠️ Could not fetch a quote today. Try again tomorrow.")
            print(f"Error fetching quote: {e}")

bot.run(TOKEN)
