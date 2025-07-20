
import discord
from discord.ext import commands
import json
import os

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_file = "roles.json"
        self.roles = self.load_roles()

    def load_roles(self):
        if os.path.exists(self.roles_file):
            with open(self.roles_file, 'r') as f:
                return json.load(f)
        return {}

    def save_roles(self):
        with open(self.roles_file, 'w') as f:
            json.dump(self.roles, f, indent=4)

    def get_member_roles(self, member):
        return self.roles.get(str(member.guild.id), {}).get(str(member.id), [])

    def has_permission(self, member, permission):
        if member.guild_permissions.administrator:
            return True
        
        member_roles = self.get_member_roles(member)
        for role_name in member_roles:
            role_permissions = self.roles.get(str(member.guild.id), {}).get("roles", {}).get(role_name, [])
            if permission in role_permissions:
                return True
        return False

    def is_owner(self, user):
        return user.id == user.guild.owner_id

    def owner_only():
        async def predicate(ctx):
            return ctx.author.id == ctx.guild.owner_id
        return commands.check(predicate)

    @commands.hybrid_group(invoke_without_command=True)
    async def role(self, ctx):
        """Manage roles and permissions."""
        await ctx.send("Invalid role command. Use `/role create`, `/role delete`, `/role assign`, `/role unassign`, or `/role list`.")

    @role.command()
    @owner_only()
    async def create(self, ctx, name: str, permissions: str):
        """Creates a new role with specified permissions."""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.roles:
            self.roles[guild_id] = {"roles": {}, "users": {}}
        
        if name in self.roles[guild_id]["roles"]:
            await ctx.send(f"Role '{name}' already exists.")
            return

        permission_list = permissions.split()
        self.roles[guild_id]["roles"][name] = permission_list
        self.save_roles()
        await ctx.send(f"Role '{name}' created with permissions: {', '.join(permission_list)}")

    @role.command()
    @owner_only()
    async def delete(self, ctx, name: str):
        """Deletes a role."""
        guild_id = str(ctx.guild.id)
        if guild_id in self.roles and name in self.roles[guild_id]["roles"]:
            del self.roles[guild_id]["roles"][name]
            # Also remove this role from any users who have it
            for user_id in self.roles[guild_id]["users"]:
                if name in self.roles[guild_id]["users"][user_id]:
                    self.roles[guild_id]["users"][user_id].remove(name)
            self.save_roles()
            await ctx.send(f"Role '{name}' deleted.")
        else:
            await ctx.send(f"Role '{name}' not found.")

    @role.command()
    @owner_only()
    async def assign(self, ctx, member: discord.Member, role_name: str):
        """Assigns a role to a member."""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in self.roles or role_name not in self.roles[guild_id]["roles"]:
            await ctx.send(f"Role '{role_name}' not found.")
            return

        if user_id not in self.roles[guild_id]["users"]:
            self.roles[guild_id]["users"][user_id] = []
        
        if role_name in self.roles[guild_id]["users"][user_id]:
            await ctx.send(f"{member.display_name} already has the role '{role_name}'.")
            return

        self.roles[guild_id]["users"][user_id].append(role_name)
        self.save_roles()
        await ctx.send(f"Assigned role '{role_name}' to {member.display_name}.")

    @role.command()
    @owner_only()
    async def unassign(self, ctx, member: discord.Member, role_name: str):
        """Unassigns a role from a member."""
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id not in self.roles or user_id not in self.roles[guild_id]["users"] or role_name not in self.roles[guild_id]["users"][user_id]:
            await ctx.send(f"{member.display_name} does not have the role '{role_name}'.")
            return

        self.roles[guild_id]["users"][user_id].remove(role_name)
        self.save_roles()
        await ctx.send(f"Unassigned role '{role_name}' from {member.display_name}.")

    @role.command()
    async def list(self, ctx):
        """Lists all available roles and their permissions."""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.roles or not self.roles[guild_id]["roles"]:
            await ctx.send("No roles have been created for this server.")
            return

        embed = discord.Embed(title="Available Roles", color=discord.Color.blue())
        for role_name, permissions in self.roles[guild_id]["roles"].items():
            embed.add_field(name=role_name, value=", ".join(permissions) or "No permissions", inline=False)
        
        await ctx.send(embed=embed)

    @role.command()
    async def myroles(self, ctx):
        """Shows your assigned roles."""
        member_roles = self.get_member_roles(ctx.author)
        if not member_roles:
            await ctx.send("You have no assigned roles.")
            return
        
        await ctx.send(f"Your roles: {', '.join(member_roles)}")

async def setup(bot):
    await bot.add_cog(Roles(bot))
