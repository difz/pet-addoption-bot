import os
import logging
from dotenv import load_dotenv
import discord

from core.engine import build_engine, respond_with_context

# -------- logging --------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -------- discord --------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
engine = build_engine()

# Per-user memory (RAM only)
MEM = {}

HELP = (
    "Hi! I'm **AdoptCare VetBot** 👩‍⚕️🐾\n"
    "Ask me about: vaccines, deworming, spay/neuter, flea/tick, diet/feeding, "
    "quarantine, vet check, behavior & introductions, home prep, costs, emergency signs.\n"
    "Tip: tell me your planned pet, e.g. `I want to adopt a 3 month old kitten`.\n"
    "_Disclaimer: I provide general guidance only, not a substitute for a veterinarian._"
)

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    text = message.content.strip()

    if text.lower() in {"!help", "/help"}:
        await message.channel.send(HELP)
        return

    ctx = MEM.setdefault(message.author.id, {"species": None, "age_months": None, "weight_kg": None})
    reply, ctx_update = respond_with_context(engine, text, ctx)
    ctx.update(ctx_update or {})

    if reply:
        logging.info(f"[{message.author}] {text} -> {reply}")
        await message.channel.send(reply)

client.run(TOKEN)
