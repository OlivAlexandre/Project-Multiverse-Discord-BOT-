import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from utils import Paginador, prefixo


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="prefixo", description="Mostra o prefixo do bot!")
    async def prefixBot(self, interaction: discord.Interaction):
        

        if interaction.guild is None:
            await interaction.response.send_message("O prefixo padrão do bot é `--`")
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT prefix FROM bot_config WHERE guild_id = ?", (interaction.guild.id,))
        result = cursor.fetchone()

        if result is None:

            cursor.execute("UPDATE bot_config SET prefix = ? WHERE guild_id = ?", ("--", interaction.guild.id))
            conn.commit()

            return await interaction.response.send_message("Nenhum prefixo personalizado encontrado para este servidor. O prefixo padrão `--` foi definido.")
        else:
            prefix = result[0]
            return await interaction.response.send_message(f"O prefixo personalizado deste servidor é: `{prefix}`")















    @app_commands.command(name="helpbot", description="Mostra a ajuda dos comandos em slash!")
    async def helpSlash(self, interaction: discord.Interaction):
        
        
        if interaction.guild is None:
            return await interaction.response.send_message(
                "Este comando não pode ser usado em mensagens diretas.", 
                ephemeral=True)

        await interaction.response.defer()
        prefixos = await prefixo(self.bot, interaction)

        guild_id = interaction.guild.id
        
        embed = discord.Embed(
            title="Help - Uso dos Slash Commands",
            description="Lista de comandos disponíveis em slash!",
            color=discord.Color.green()
        )
        if interaction.guild.icon:
            embed.set_image(url=interaction.guild.icon.url)
        else:
            embed.set_image(url=interaction.bot.user.avatar.url)

        embed.add_field(name="`/teste`", value="Verifica se o bot está funcionando corretamente.", inline=False)
        embed.add_field(name="`/donate`", value ="Mostra informações sobre como apoiar o criador do bot.", inline=False)
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute("SELECT command_name, type_archive, type_command FROM custom_command WHERE guild_id = ?", (guild_id,))
        custom_commands = cursor.fetchall()
        conn.close()

        if not custom_commands:
            await interaction.followup.send(embed=embed)
            return

        embed_custom = discord.Embed(
            title="Comandos Personalizados",
            description="Aqui você verá todos os comandos personalizados disponíveis neste servidor.",
            color=discord.Color.blue()
        )

        for nome_comando, tipo_arquivo, tipo_comando in custom_commands:
            embed_custom.add_field(name=f"`{prefixos}{nome_comando}`", value=f"Tipo do comando: {tipo_arquivo}", inline=False)

        if interaction.guild.icon:
            embed_custom.set_image(url=interaction.guild.icon.url)
        else:
            embed_custom.set_image(url=interaction.bot.user.avatar.url)

        lista = [embed, embed_custom]
        view = Paginador(paginas=lista)
        await interaction.followup.send(embed=lista[0], view=view)















    @app_commands.command(name="teste", description="Testa o bot em slash.")
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("# `Bot funcionando corretamente!`")















    @app_commands.command(name="donate", description="Gostou do bot? Apoie o criador do bot!")
    async def donate(self, interaction: discord.Interaction):
        dono_bot = self.bot.get_user(444994237080141845)
        embed = discord.Embed(
            title="Apoie o Criador do Bot!",
            description="Se você gostou do bot, considere apoiar o criador!",
            color=discord.Color.blue()
        )
        embed.add_field(name=f"Opção única: Pix do criador ({dono_bot.mention})", value="📱 Chave Pix: `(81) 99853-0702`", inline=False)
        embed.add_field(name="Frase de efeito:", value="`O multiverse me fez feliz, no início me senti limitado, mas depois se tornou um lar para mi, e nada mais justo que tornar o servidor feliz com a minha criação`", inline=False)
        embed.set_image(url=self.bot.user.avatar.url)
        embed.set_footer(text="Agradeço a todos que apoiarem! 💖")
        await interaction.response.send_message(embed=embed, ephemeral=True)



    










    



    @app_commands.command(name="ping", description="Mostra a latência do bot")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! Latência: {round(self.bot.latency * 1000)} ms")






async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
