import discord
from discord.ext import commands

class op(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)  # 檢查是否具有管理員權限
    @commands.is_owner()  # 檢查是否為機器人的擁有者
    async def say(self, ctx, *, msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def clear(self, ctx, member: discord.Member, num: int = 10):
        def is_member_message(message):
            return message.author == member

        deleted = await ctx.channel.purge(limit=num, check=is_member_message)
        await ctx.send(f'成功刪除 {len(deleted)} 條 {member.mention} 的訊息！')



    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def clear(self, ctx, target: str = "all"):
        if target.lower() == "all":
            await ctx.channel.purge()
            await ctx.send('成功刪除所有訊息！')
        else:
            member = ctx.message.mentions[0]
            def is_member_message(message):
                return message.author == member

            deleted = await ctx.channel.purge(limit=10, check=is_member_message)
            await ctx.send(f'成功刪除 {len(deleted)} 條 {member.mention} 的訊息！')

        


def setup(bot):
    bot.add_cog(op(bot))
