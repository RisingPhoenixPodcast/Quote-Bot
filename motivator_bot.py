import discord
from discord.ext import tasks, commands
import datetime
import random
import os

# Get environment variables from Railway
TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Curated motivational quotes
quotes = [
    {"text": "You are not broken. You are healing.", "author": "Unknown"},
    {"text": "This pain will shape you — but it doesn’t define you.", "author": "You"},
    {"text": "Grief is just love with nowhere to go.", "author": "Jamie Anderson"},
    {"text": "Radical ownership is the beginning of peace.", "author": "You"},
    {"text": "You didn’t fail — you outgrew who you were pretending to be.", "author": "Unknown"},
    {"text": "Letting go is not giving up. It's choosing yourself.", "author": "You"},
    {"text": "You are still worthy of love, even if someone else couldn’t give it.", "author": "You"},
    {"text": "You’re not starting over — you’re starting stronger.", "author": "Unknown"},
    {"text": "Every morning you get back up is a win.", "author": "You"},
    {"text": "You can’t heal what you won’t feel.", "author": "You"},
    {"

            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()
            quote = data[0]['q']
            author = data[0]['a']
            await channel.send(f"🌟 **Daily Motivation** 🌟\n> *{quote}*\n\n— **{author}**")
        except Exception as e:
            await channel.send("⚠️ Could not fetch a quote today. Try again tomorrow.")
            print(f"Error fetching quote: {e}")

bot.run(TOKEN)
