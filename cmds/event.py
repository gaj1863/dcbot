import discord
from discord.ext import commands

welcome_channel_id = 984375391986790450  # 替換為您的歡迎頻道的ID
goodbye_channel_id = 984375391986790450  # 替換為您的離開頻道的ID
target_guild_id = 816905130523885598  # 替換為目標伺服器的ID

class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # 新成員加入時的處理
        if member.guild.id == target_guild_id:
            welcome_channel = self.bot.get_channel(welcome_channel_id)

            # 獲取所在伺服器的總人數（排除機器人）
            guild = member.guild
            total_members = len(guild.members) - sum(1 for member in guild.members if member.bot)

            # 獲取機器人成員數量
            bot_count = sum(1 for member in guild.members if member.bot)

            # 建立嵌入訊息
            embed = discord.Embed(
                title='歡迎加入伺服器！',
                description=f'歡迎 {member.mention} 加入伺服器！\n總人數：{total_members}\n機器人數量：{bot_count}',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar_url)

            await welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # 成員離開時的處理
        if member.guild.id == target_guild_id:
            goodbye_channel = self.bot.get_channel(goodbye_channel_id)

            # 獲取所在伺服器的總人數（排除機器人）
            guild = member.guild
            total_members = len(guild.members) - sum(1 for member in guild.members if member.bot)

            # 獲取機器人成員數量
            bot_count = sum(1 for member in guild.members if member.bot)

            # 建立嵌入訊息
            embed = discord.Embed(
                title='成員離開',
                description=f'{member.name} 離開了伺服器。\n總人數：{total_members}\n機器人數量：{bot_count}',
                color=discord.Color.red()
            )
            embed.set_thumbnail(url=member.avatar_url)

            await goodbye_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(event(bot))
