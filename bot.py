import discord
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

# Token & Channel-ID kommen aus Railway Variablen
TOKEN = os.getenv("MTQxMTQzNjM5NTQ3MzY3MDIzNg")
CHANNEL_ID = int(os.getenv("1411452316699197542"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
scheduler = AsyncIOScheduler(timezone="Europe/Berlin")

# Essen + Wahrscheinlichkeiten
FOODS = [
    ("Spinat", 0.55, "Heute ist Spinattag! Yippie!"),
    ("Pizza", 0.25, "Heute ist Pizzatag! Guten Appetit!"),
    ("Pommes", 0.15, "Heute gibt es Pommes! 🍟"),
    ("Gulasch", 0.0025, "Wow, heute gibt es Gulasch! Seltenheit pur!"),
    ("Buchstabensuppe", 0.0025, "Heute gibt es Buchstabensuppe! 🔤🍲"),
    ("Nesquik", 0.0025, "Überraschung! Nesquik-Tag 🥛🍫"),
]

last_food = None  # merken, was gestern war
streak = 0        # wie viele Tage in Folge das gleiche Essen war

def pick_food():
    global last_food, streak

    # Extra-Logik: Spinat darf öfter hintereinander kommen
    if last_food == "Spinat" and streak < 2:
        streak += 1
        return "Spinat", "Heute ist Spinattag! Yippie!"
    else:
        # normale Zufallsauswahl nach Gewicht
        names = [f[0] for f in FOODS]
        weights = [f[1] for f in FOODS]
        choice = random.choices(FOODS, weights=weights, k=1)[0]
        food, _, message = choice

        if food == last_food:
            streak += 1
        else:
            streak = 1
        last_food = food
        return food, message

async def send_daily_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("❗ Channel nicht gefunden – stimmt die ID?")
        return

    _, message = pick_food()
    await channel.send(message)

@client.event
async def on_ready():
    print(f"✅ Eingeloggt als {client.user}")
    scheduler.add_job(send_daily_message, "cron", hour=9, minute=0)
    scheduler.start()
    print("⏰ Tägliche Vorhersage für 09:00 geplant (Berlin-Zeit).")

client.run(TOKEN)
