import discord
from discord.ext import tasks, commands
import datetime
import random
import os
import json

# Load curated quotes from quotes.json
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes = json.load(f)

# Get environment variables from Railway
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



