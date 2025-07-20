import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Kicks a member from the server."""
        if member == self.bot.user:
            await ctx.send("I can't kick myself!")
            return
        if member == ctx.author:
            await ctx.send("You can't kick yourself!")
            return
        
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} has been kicked for: {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that!")

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Bans a member from the server."""
        if member == self.bot.user:
            await ctx.send("I can't ban myself!")
            return
        if member == ctx.author:
            await ctx.send("You can't ban yourself!")
            return

        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned for: {reason}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to do that!")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
