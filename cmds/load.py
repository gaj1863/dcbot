import discord
from discord.ext import commands

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loaded_cogs = []

    def setup(self, bot):
        for cog in self.loaded_cogs:
            bot.add_cog(cog)

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, extension):
        # 加載 Cog 並記錄
        cog = self.bot.load_extension(extension)
        self.loaded_cogs.append(cog)
        await ctx.send(f'加載 {extension} 完成.')

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx, extension):
        # 卸載 Cog 並更新記錄
        cog = self.bot.unload_extension(extension)
        self.loaded_cogs.remove(cog)
        await ctx.send(f'卸載 {extension} 完成.')

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx, extension):
        # 重新加載 Cog
        cog = self.bot.reload_extension(extension)
        await ctx.send(f'重新加載 {extension} 完成.')

    @commands.is_owner()
    @commands.command()
    async def list_cogs(self, ctx):
        all_cogs_names = [cog.__class__.__name__ for cog in self.bot.cogs.values()]
        loaded_cogs_names = [cog.__class__.__name__ for cog in self.loaded_cogs]

        # 重新查詢 Bot 目前已載入的 Cogs
        actual_loaded_cogs = [cog.__class__.__name__ for cog in self.bot.cogs.values()]

        unloaded_cogs = set(all_cogs_names) - set(actual_loaded_cogs)
        await ctx.send(f'所有 Cogs:  {", ".join(all_cogs_names)}\n目前載入的 Cogs: {", ".join(loaded_cogs_names)}\n未載入的 Cogs: {", ".join(unloaded_cogs)}')
        

def setup(bot):
    cog = owner(bot)
    bot.add_cog(cog)
    cog.setup(bot)
