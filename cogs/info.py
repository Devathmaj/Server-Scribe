import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Displays information about a server member."""
        if member is None:
            member = ctx.author

        embed = discord.Embed(title=f"User Information for {member.name}", color=member.color)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="Username", value=member.display_name, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, style='F'), inline=False)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined_at, style='F'), inline=False)
        
        roles = [role.mention for role in member.roles[1:]] # Exclude @everyone
        if roles:
            embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles), inline=False)
        else:
            embed.add_field(name="Roles", value="No roles.", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def serverinfo(self, ctx):
        """Displays information about the server."""
        guild = ctx.guild

        embed = discord.Embed(title=f"Server Information for {guild.name}", color=discord.Color.green())
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
            
        embed.add_field(name="Server Name", value=guild.name, inline=True)
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=str(guild.member_count), inline=True)
        embed.add_field(name="Text Channels", value=str(len(guild.text_channels)), inline=True)
        embed.add_field(name="Voice Channels", value=str(len(guild.voice_channels)), inline=True)
        embed.add_field(name="Created At", value=discord.utils.format_dt(guild.created_at, style='F'), inline=False)
        
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
