import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from utils import Paginador, whitelist_adm_prefix, prefixo


class PrefixC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.group(name="prefix", description="[STAFF] Gerencia os prefixos do servidor.", invoke_without_command=True)
    @whitelist_adm_prefix()
    async def prefix_group(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        await ctx.send(f"Especifique a ação do prefixo: Use `{prefixo_prefix}prefix [set/view/reset]`")
    















    @prefix_group.command(name="help", description="[STAFF] Mostra ajuda sobre os comandos de prefixo.")
    @whitelist_adm_prefix()
    async def helpprefix(self, ctx: commands.Context):

        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas", ephemeral=True)
            return
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT prefix FROM bot_config WHERE guild_id = ?", (ctx.guild.id,))
        prefixo = cursor.fetchone()
        
        embed = discord.Embed(
            title="Ajuda dos Comandos de Prefixo (Admin)",
            description="Aqui estão os comandos disponíveis para administrar os prefixos:",
            color=discord.Color.blue()
        )
        embed.add_field(name=f"{prefixo_prefix}prefix set <prefix>", value="Adiciona um novo prefixo para o servidor.", inline=False)
        embed.add_field(name=f"{prefixo_prefix}prefix view", value="Vê o prefixo configurado do servidor.", inline=False)
        embed.add_field(name=f"{prefixo_prefix}prefix reset", value="Reseta o prefixo do servidor para o padrão do bot (--)", inline=False)
        await ctx.send(embed=embed)















    @prefix_group.command(name="set", description="[STAFF] Define um novo prefixo para o servidor.")
    @app_commands.describe(prefix="O novo prefixo para o servidor")
    @app_commands.checks.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context, prefix: str):

        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return

        prefix = prefix.strip()
        if not prefix:
            await ctx.send("O prefixo não pode ser vazio. Por favor, forneça um prefixo válido.", ephemeral=True)
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO bot_config (guild_id, prefix) VALUES (?, ?)''',
                       (ctx.guild.id, prefix))
        conn.commit()
        conn.close()
        await ctx.send(f"Prefixo atualizado para: `{prefix}`")
    














    @prefix_group.command(name="view", description="Vê o prefixo configurado do servidor.")
    @whitelist_adm_prefix()
    async def viewprefix(self, ctx: commands.Context):

        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas", ephemeral=True)
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT prefix FROM bot_config WHERE guild_id = ?", (ctx.guild.id,))
        result = cursor.fetchone()

        if result is None:

            cursor.execute("UPDATE bot_config SET prefix = ? WHERE guild_id = ?", ("--", ctx.guild.id))
            conn.commit()

            return await ctx.send("Nenhum prefixo personalizado encontrado para este servidor. O prefixo padrão é `--`.")
        else:
            prefix = result[0]
            return await ctx.send(f"O prefixo personalizado deste servidor é: `{prefix}`")
    














    @prefix_group.command(name="reset", description="[STAFF] Reseta o prefixo do servidor para o padrão.")
    @app_commands.checks.has_permissions(administrator=True)
    async def resetprefix(self, ctx: commands.Context):

        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas", ephemeral=True)
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT prefix FROM bot_config WHERE guild_id = ?", (ctx.guild.id,))
        result = cursor.fetchone()

        if result is None:
            await ctx.send("Nenhum prefixo personalizado encontrado para este servidor.", ephemeral=True)
        else:
            prefix = result[0]
            cursor.execute("UPDATE bot_config SET prefix = ? WHERE guild_id = ?", ("--", ctx.guild.id))
            conn.commit()
            await ctx.send(f"Prefixo resetado para o padrão: `{prefix}`")






async def setup(bot):
    await bot.add_cog(PrefixC(bot))