import discord
from discord.ext import commands

class AddRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def add_role(self, ctx, role_id: int):
        try:
            role = ctx.guild.get_role(role_id)
            if role:
                for member in ctx.guild.members:
                    await member.add_roles(role)
                await ctx.send(f"Successfully added role {role.name} to all members.")
            else:
                await ctx.send("Role not found.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

def setup(bot):
    bot.add_cog(AddRoleCog(bot))
