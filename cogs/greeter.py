import discord
from discord.ext import commands

class Greeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Greets a new member in the system channel."""
        if member.bot:
            return
            
        channel = member.guild.system_channel
        if channel is not None:
            embed = discord.Embed(
                title=f"Welcome to {member.guild.name}, {member.name}!",
                description=f"We're glad to have you here. Please read the rules and enjoy your stay!",
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Greeter(bot))
