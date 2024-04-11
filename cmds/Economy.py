import discord
import json
import os
import matplotlib.pyplot as plt
import random
import time
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, owner_id=543290770283692042)

rpg_data = {}  # 用於儲存玩家的等級、經驗值、金錢資訊

with open('setting.json', mode='r', encoding='utf-8') as jfile:
    jdata = json.load(jfile)


class Inquire(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # 忽略機器人的訊息
            return

        user_id = str(message.author.id)
        current_time = time.time()
        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit(current_time)
        if retry_after:
            return  # 冷卻中，忽略訊息
        else:
            if user_id not in rpg_data:
                rpg_data[user_id] = {'level': 1, 'exp': 0, 'balance': 0, 'exp_to_next_level': 100}  # 創建新的玩家資料
                save_data_to_json()  # 儲存資料

            exp_gain = random.randint(10, 20)  # 隨機獲得10到20的經驗值
            rpg_data[user_id]['exp'] += exp_gain
            await check_level_up(message.author, message.channel)  # 檢查是否升級
            
            save_data_to_json()  # 儲存資料

    @commands.command(name='info', description='查詢成員資料')
    async def get_member_info(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        user_id = str(member.id)
        if user_id in rpg_data:
            level = int(rpg_data[user_id]['level'])
            exp = int(rpg_data[user_id]['exp'])
            exp_to_next_level = int(rpg_data[user_id]['exp_to_next_level'])
            progress_percentage = calculate_progress_percentage(exp, exp_to_next_level)
            balance = int(rpg_data[user_id]['balance'])

            embed = discord.Embed(title=f"{member.name} 的資料", color=0x00FF00)
            embed.add_field(name="等級", value=str(level), inline=True)
            embed.add_field(name="進度", value=f"{exp}/{exp_to_next_level}", inline=True)
            embed.add_field(name="百分比", value=f"{progress_percentage:.2f}%", inline=False)
            embed.add_field(name="金錢", value=f"{balance}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("找不到該成員的資料。")


    @commands.command(name='ranking', description='查詢等級排行榜')
    async def get_level_ranking(self, ctx):
        sorted_levels = sorted(rpg_data.items(), key=lambda x: x[1]['level'], reverse=True)
        
        embed = discord.Embed(title='等級排行榜', color=discord.Color.gold())
        for index, (user_id, data) in enumerate(sorted_levels[:10]):
            member = self.bot.get_user(int(user_id))
            if member:
                level = int(rpg_data[user_id]['level'])
                exp = int(rpg_data[user_id]['exp'])
                exp_to_next_level = int(rpg_data[user_id]['exp_to_next_level'])
                percentage = calculate_progress_percentage(exp, exp_to_next_level)
                
                embed.add_field(name=f'第 {index+1} 名', value=f'{member.mention} 等級: **{level}**  ({percentage:.1f}%)', inline=False)

        await ctx.send(embed=embed)
        save_data_to_json()  # 儲存資料

        


async def check_level_up(user, channel):
    user_id = str(user.id)
    if user_id in rpg_data:
        exp = rpg_data[user_id]['exp']
        level = rpg_data[user_id]['level']
        exp_to_next_level = rpg_data[user_id]['exp_to_next_level']
        if exp >= exp_to_next_level:
            rpg_data[user_id]['level'] += 1
            rpg_data[user_id]['exp'] -= exp_to_next_level
            rpg_data[user_id]['exp_to_next_level'] = (level+1)*100
            await channel.send(f'{user.mention} 升級了！({rpg_data[user_id]["level"]})')

            target_channel_id = 928290407895404574  # 更換為有效的頻道 ID
            target_channel = bot.get_channel(target_channel_id)
            if target_channel is not None:
                await target_channel.send(f'{user.mention} 升級了！({rpg_data[user_id]["level"]})')

            save_data_to_json()  # 儲存資料


def calculate_progress_percentage(current_exp, exp_to_next_level):
    # 計算進度百分比
    return round(current_exp / exp_to_next_level * 100, 2)


def save_data_to_json():
    with open('data.json', mode='w', encoding='utf-8') as jfile:
        json.dump(rpg_data, jfile, indent=4, ensure_ascii=False)


def load_data_from_json():
    global rpg_data
    try:
        with open('data.json', mode='r', encoding='utf-8') as jfile:
            rpg_data = json.load(jfile)
    except FileNotFoundError:
        save_data_to_json()  # 建立空白的 JSON 檔案
        return
    except json.decoder.JSONDecodeError:
        save_data_to_json()  # 建立空白的 JSON 檔案
        return


def setup(bot):
    load_data_from_json()  # 載入資料
    bot.add_cog(Inquire(bot))
