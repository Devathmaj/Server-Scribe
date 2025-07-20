import discord
from discord.ext import commands
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        # Ensure the session is closed when the cog is unloaded
        self.bot.loop.create_task(self.session.close())

    @commands.hybrid_command()
    async def ping(self, ctx):
        """Checks the bot's latency."""
        latency = self.bot.latency * 1000  # Convert to milliseconds
        await ctx.send(f"Pong! 🏓 Latency: {latency:.2f}ms")

    @commands.hybrid_command()
    async def joke(self, ctx):
        """Fetches a random programming joke."""
        await ctx.defer()
        try:
            async with self.session.get(
                "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single"
            ) as response:
                response.raise_for_status()
                joke_data = await response.json()

                if joke_data.get("error"):
                    await ctx.send("Sorry, I couldn't fetch a joke at the moment. Please try again later.")
                    return

                embed = discord.Embed(
                    title="Programming Joke",
                    description=joke_data.get("joke"),
                    color=discord.Color.blue()
                )
                await ctx.send(embed=embed)

        except aiohttp.ClientError as e:
            print(f"Error fetching joke: {e}")
            await ctx.send("Sorry, I couldn't connect to the joke service.")

async def setup(bot):
    await bot.add_cog(Fun(bot))
