import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pages = [
            discord.Embed(title="指令表:", color=0x11ff00),
            discord.Embed(title="指令表:", description="(小遊戲)", color=0x00ff27),
            discord.Embed(title="指令表:", description="(使用者需要管理權限)", color=0x00ff27),
            discord.Embed(title="指令表:", description="(限開發人員)", color=0x00ff27)
        ]
        self.current_page = 0

        self.pages[0].add_field(name="ping", value="檢查 Bot 目前的延遲", inline=True)
        self.pages[0].add_field(name="bot", value="給用戶提供 Bot 的資訊", inline=False)
        self.pages[0].add_field(name="info", value="查詢成員資料", inline=False)
        self.pages[0].add_field(name="ranking", value="查詢等級排行榜(前10名)", inline=False)
    
        
        self.pages[1].add_field(name="運勢", value="訊息中只要有即可觸發", inline=True)
        
        

        self.pages[2].add_field(name="say", value="訊息複誦", inline=False)
        self.pages[2].add_field(name="clear", value="清理該頻道訊息，可自訂義數量\n$clear @成員 數量,沒打數量預設10", inline=False)
        self.pages[2].add_field(name="clear all", value="清理該頻道所有訊息", inline=False)
    

        self.pages[3].add_field(name="load", value="加載檔案", inline=False)
        self.pages[3].add_field(name="unload", value="卸載檔案", inline=False)
        self.pages[3].add_field(name="reload", value="重新加載檔案", inline=False)
    

    @commands.command()
    async def help(self, ctx):
        embed = self.pages[self.current_page]
        embed.set_footer(text=f"頁數 {self.current_page+1}/{len(self.pages)}")

        message = await ctx.send(embed=embed)
        # 使用數字按鈕
        for i in range(1, len(self.pages) + 1):
            await message.add_reaction(f"{i}\N{combining enclosing keycap}")

        def check(reaction, user):
            return (
                user == ctx.author
                and str(reaction.emoji) in [f"{i}\N{combining enclosing keycap}" for i in range(1, len(self.pages) + 1)]
                and reaction.message.id == message.id
            )

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=None, check=check
                )
            except TimeoutError:
                break

            # 將數字轉換為頁碼（從1開始）
            selected_page = int(reaction.emoji[0])

            self.current_page = max(min(selected_page - 1, len(self.pages) - 1), 0)

            embed = self.pages[self.current_page]
            embed.set_footer(text=f"頁數 {self.current_page+1}/{len(self.pages)}")
            await message.edit(embed=embed)
            await message.remove_reaction(reaction, user)

        await message.clear_reactions()

def setup(bot):
    bot.add_cog(HelpCog(bot))
