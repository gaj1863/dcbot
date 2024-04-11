import discord
from discord.ext import commands

rpg_data = {}

class Cmd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"目前延遲: {round(self.bot.latency*1000)} 毫秒")

    @commands.command()
    async def bot(self, ctx):
        embed = discord.Embed(title="**---------------武神bot---------------**", description=" ", color=0x00ff27)
        embed.add_field(name="\n開發者", value="wu_god")
        embed.add_field(name="\n服務器數量", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="\n邀請BOT", value="[點擊](https://discord.gg/rkaats8Bh2)")
        embed.add_field(name="\n ", value=f"在文字頻道發送消息獲得成員經驗值10~20\n此BOT還在開發中.\n")
        await ctx.send(embed=embed)
        



def setup(bot):
    bot.add_cog(Cmd(bot))
