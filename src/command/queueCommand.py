import discord
import datetime
from discord import app_commands
from discord.ext import commands
from typing import List
from service.AudioService import get_queue, get_now_playing_title 
from model.AudioModel import AudioModel

class QueueView(discord.ui.View):
    def __init__(self, queue: List[AudioModel], now_playing_title: str, user: discord.User):
        super().__init__()
        self.queue = queue
        self.now_playing_title = now_playing_title
        self.user = user
        self.current_page = 0
        self.items_per_page = 10
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        if self.current_page > 0:
            self.add_item(PrevButton())
        if (self.current_page + 1) * self.items_per_page < len(self.queue):
            self.add_item(NextButton())

    async def update_message(self, interaction: discord.Interaction):
        start = self.current_page * self.items_per_page
        end = start + self.items_per_page
        queue_titles = [f"{start + i + 1}. {item.get_title()}" for i, item in enumerate(self.queue[start:end])]
        description = f"現在再生中の曲: {self.now_playing_title}\n\n" + "\n".join(queue_titles)
        embed = discord.Embed(
            title="キュー",
            description=description,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        await interaction.response.edit_message(embed=embed, view=self)

class PrevButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='前のページ', style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view: QueueView = self.view
        if interaction.user != view.user:
            return await interaction.response.send_message("あなたはこのボタンを押す権限がありません。", ephemeral=True)
        view.current_page -= 1
        view.update_buttons()
        await view.update_message(interaction)

class NextButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='次のページ', style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        view: QueueView = self.view
        if interaction.user != view.user:
            return await interaction.response.send_message("あなたはこのボタンを押す権限がありません。", ephemeral=True)
        view.current_page += 1
        view.update_buttons()
        await view.update_message(interaction)

class QueueCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name="queue", description="キューを表示します")
    async def queue(self, interaction: discord.Interaction):
        queue = get_queue(interaction.guild)
        if not queue:
            await interaction.response.send_message("キューに曲がありません。", ephemeral=True)
            return
        
        now_playing_title = get_now_playing_title(interaction.guild)
        queue = queue[1:]
        queue_titles = [f"{i+1}. {item.get_title()}" for i, item in enumerate(queue[:10])]
        description = f"現在再生中の曲: {now_playing_title}\n\n" + "\n".join(queue_titles)
        embed = discord.Embed(
            title="キュー",
            description=description,
            color=discord.Color.blue(),
            timestamp=datetime.datetime.now()
        )
        view = QueueView(queue, now_playing_title, interaction.user)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(QueueCommand(bot))
