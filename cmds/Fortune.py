import discord
from discord.ext import commands
import random

class FortuneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fortunes = ['大吉', '中吉', '小吉', '末吉', '你不要知道比較好','大凶', '中凶', '小凶', '末凶']  # 運勢列表

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.endswith('運勢'):
            await self.send_fortune(message)

    async def send_fortune(self, message):
        user = message.author
        fortune = random.choice(self.fortunes)  # 隨機選取一個運勢

        response = f'{user.mention} \n {message.content} ： {fortune}'
        await message.channel.send(response)


def setup(bot):
    bot.add_cog(FortuneCog(bot))
