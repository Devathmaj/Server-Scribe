import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import pathlib

# --- CONFIGURATION ---
# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# --- PATHS ---
BASE_DIR = pathlib.Path(__file__).parent
COGS_DIR = BASE_DIR / "cogs"

# --- BOT SETUP ---
# Define intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

# --- EVENTS ---
@bot.event
async def on_ready():
    """Event that fires when the bot is ready and connected to Discord."""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    print('Bot is ready and online!')
    # Synchronize the commands
    await bot.tree.sync()
    print('Commands have been synced.')

# --- COG LOADING ---
async def load_cogs():
    """Loads all cogs from the cogs directory."""
    for filename in os.listdir(COGS_DIR):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

# --- BOT RUN ---
async def main():
    if TOKEN is None:
        print("ERROR: DISCORD_TOKEN environment variable not found.")
        print("Please create a .env file and add your bot token.")
        return

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())