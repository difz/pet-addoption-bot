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
    "👋 Hi! I'm **AdoptCare VetBot** 🐾\n\n"
    "**How to use me:**\n"
    "• To ask a question, type: `!ask your question here`\n"
    "   e.g. `!ask I want to adopt a 3 month old kitten`\n"
    "• Use `!help` anytime to see this guide again.\n\n"
    "**Topics I can help with:**\n"
    "• Vaccines & deworming\n"
    "• Spay / neuter\n"
    "• Flea & tick treatment\n"
    "• Diet & feeding\n"
    "• Quarantine & vet check\n"
    "• Behavior & introductions\n"
    "• Home preparation\n"
    "• Adoption costs\n"
    "• Emergency signs 🚨\n\n"
    "_Disclaimer: I provide general guidance only — not a substitute for a licensed veterinarian._"
)

@client.event
async def on_ready():
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    text = message.content.strip()

    # hanya respon kalau text diawali "!" atau "/"
    if not (text.startswith("!") or text.startswith("/")):
        return

    # === help ===
    if text.lower() in {"!help", "/help"}:
        await message.channel.send(HELP)
        return

    # === ask ===
    if text.lower().startswith(("!ask", "/ask")):
        # ambil query setelah "!ask " atau "/ask "
        query = text.split(maxsplit=1)
        if len(query) < 2:
            await message.channel.send("Please provide a question, e.g. `!ask my cat has fleas`")
            return

        query_text = query[1]

        ctx = MEM.setdefault(message.author.id, {"species": None, "age_months": None, "weight_kg": None})
        reply, ctx_update = respond_with_context(engine, query_text, ctx)
        ctx.update(ctx_update or {})

        if reply:
            logging.info(f"[{message.author}] {query_text} -> {reply}")
            await message.channel.send(reply)


client.run(TOKEN)
