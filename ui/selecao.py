import discord
import sqlite3
from discord.ext import commands
from discord import app_commands


class escolha(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=60)
        self.bot = bot
        self.value = None

    @discord.ui.button(label="Aceitar", style=discord.ButtonStyle.green)
    async def solo(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "accept"
        await interaction.response.send_message("Você escolheu aceitar o convite!", ephemeral=True)
        self.stop()

    @discord.ui.button(label="Negar", style=discord.ButtonStyle.blurple)
    async def player(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "deny"
        await interaction.response.send_message("Você escolheu negar o convite!", ephemeral=True)
        self.stop()


class escolhaButtons(discord.ui.View):
    def __init__(self, bot):
        super().___init__(timeout=60)
        self.bot = bot
        self.value = None
    

    @discord.ui.button(label="Lutar", style=discord.ButtonStyle.red)
    async def lutar(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "lutar"
        await interaction.response.send_message("Você escolheu lutar!", ephemeral=True)
    
    @discord.ui.button(label="Interagir", style=discord.ButtonStyle.blurple)
    async def interagir(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "interagir"
        await interaction.response.send_message("Você escolheu interagir!", ephemeral=True)
    
    @discord.ui.button(label="Itens", style=discord.ButtonStyle.gray)
    async def itens(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "itens"
        await interaction.response.send_message("Você escolheu abrir o inventário!", ephemeral=True)

    @discord.ui.button(label="Fugir", style=discord.ButtonStyle.green)
    async def fugir(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = "fugir"
        await interaction.response.send_message("Você escolheu fugir!", ephemeral=True)