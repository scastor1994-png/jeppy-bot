import os
import random
import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import pytz

from flask import Flask
from threading import Thread

# --- Keep Alive Webserver ---
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Discord Bot Setup ---
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

tz = pytz.timezone("Europe/Berlin")

def choose_food():
    r = random.random()
    if r < 0.70:
        return "Heute ist Spinattag! 🥬 Yippie!"
    elif r < 0.90:
        return "Heute gibt’s Pizza! 🍕"
    elif r < 0.98:
        return "Pommes-Tag! 🍟"
    elif r < 0.989:
        return "Oh wow, Gulasch! 🍲"
    elif r < 0.998:
        return "Buchstabensuppe-Tag! 🍜"
    else:
        return "Überraschung: Nesquik! 🥛"

@client.event
async def on_ready():
    print(f"Eingeloggt als {client.user}")
    send_daily_message.start()

@tasks.loop(minutes=1)
async def send_daily_message():
    now = datetime.now(tz)
    if now.hour == 9 and now.minute == 0:  # genau 09:00 Uhr
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(choose_food())

# --- Start ---
keep_alive()
client.run(TOKEN)
