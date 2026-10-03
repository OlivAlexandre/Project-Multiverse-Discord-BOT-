import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
from utils import whitelist_adm_slash
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

timezone = ZoneInfo("America/Sao_Paulo")
agora = datetime.now(timezone)

class autocommandsGroup(app_commands.Group, name="autocommand", description="Seta comandos automáticos"):


    @app_commands.command(name="set", description="Seta de maneira automática um comando customizado a executar")
    @app_commands.choices(tipo=[
        app_commands.Choice(name="Horário fixo (ex.: 05:00 / 12:00)", value="diario"),
        app_commands.Choice(name="Intervalos (ex.: A cada x minutos)", value="intervalo")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(tipo="Escolha o tipo de execução do comando",
                           tempo="Escolha o horário ou intervalo de execução do comando",
                           canal="Escolha o canal onde o comando será executado",
                           nome_comando="Escolha o comando que deseja executar de maneira automática",
                           ping="Escolha o cargo que deseja mencionar no comando")
    async def setcommand(self, interaction: discord.Interaction, nome_comando: str, tipo: str, tempo: str, canal: discord.TextChannel = None, ping: discord.Role = None):

        await interaction.response.defer(ephemeral=True)
        role_id = ping.id if ping else None
        canal_alvo = canal or interaction.channel

        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()

        cursor.execute("SELECT command_name FROM custom_command WHERE guild_id = ? AND command_name = ?", (interaction.guild.id, nome_comando))
        custom = cursor.fetchone()



        nativo = interaction.client.get_command(nome_comando) or interaction.client.tree.get_command(nome_comando)
        if nativo is not None:
            
            cursor.execute("""INSERT INTO automatico (guild_id, canal_id, nome_comando, tipo, tempo, role_id)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                            (interaction.guild.id, canal_alvo.id, nome_comando, tipo, tempo, role_id))
            conn.commit()

            await interaction.followup.send(
                f"--- Automação feita com sucesso!!---\n\n"
                f"Comando: `{nome_comando}`\n"
                f"Modo: `{tipo.capitalize()}` (`{tempo}`)\n"
                f"Canal de envio/local: {canal_alvo.mention}\n"
                "***Comando nativo setado com sucesso!!!***"
            )

        elif custom is not None:

            cursor.execute("""INSERT INTO automatico (guild_id, canal_id, nome_comando, tipo, tempo, role_id)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                            (interaction.guild.id, canal_alvo.id, nome_comando, tipo, tempo, role_id))
            conn.commit()
    
            await interaction.followup.send(
                f"--- Automação feita com sucesso!!---\n\n"
                f"Comando: `{nome_comando}`\n"
                f"Modo: `{tipo.capitalize()}` (`{tempo}`)\n"
                f"Canal de envio/local: {canal_alvo.mention}\n"
                "***Comando personalizado setado com sucesso!!!***"
            )

        else:
            return await interaction.followup.send("Oh não! Você não tem este comando setado conosco! Sinto muito . . .", ephemeral=True)




        
    









    @app_commands.command(name="remove", description="Remove um comando automático setado")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(nome_comando="Escolha o comando que deseja remover da automação")
    async def removecommand(self, interaction: discord.Interaction, nome_comando: str):
        await interaction.response.defer(ephemeral=True)

        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nome_comando FROM automatico WHERE guild_id = ?", (interaction.guild.id,))
        existing_commands = [row[0] for row in cursor.fetchall()]

        if nome_comando not in existing_commands:
            return await interaction.followup.send("Ops! Você não tem este comando ou ele foi deletado!", ephemeral=True)

        cursor.execute("DELETE FROM automatico WHERE guild_id = ? AND nome_comando = ?", (interaction.guild.id, nome_comando))
        conn.commit()

        await interaction.followup.send(f"--- Comando automático removido com sucesso! ---\n\nComando: `{nome_comando}`")



    




    @app_commands.command(name="list", description="Lista todos os comandos automáticos setados")
    @app_commands.checks.has_permissions(administrator=True)
    async def listcommands(self, interaction: discord.Interaction):

        await interaction.response.defer(ephemeral=False)

        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()

        cursor.execute("SELECT canal_id, nome_comando, tipo, tempo, role_id FROM automatico WHERE guild_id = ?", (interaction.guild.id,))
        commands_list = cursor.fetchall()

        if not commands_list:
            await interaction.followup.send("Nenhum comando automático setado neste servidor.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Comandos Automáticos",
            description="Lista de comandos automáticos com suas configurações.",
            color=discord.Color.blue()
        )

        

        for canal_id, nome_comando, tipo, tempo, role_id in commands_list:
            ping = interaction.guild.get_role(role_id) if role_id else None
            ping_role = ping.mention if ping else "Nenhum cargo mencionado"
            canal = interaction.guild.get_channel(canal_id)
            canal_mention = canal.mention if canal else "Canal não encontrado"

            if tipo.lower() == "diario":
                hora, minuto = map(int, tempo.split(":"))
                execução_prevista = agora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
                if execução_prevista <= agora:
                    execução_prevista += timedelta(days=1)

            elif tipo.lower() == "intervalo":
                minutos = int(tempo)
                execução_prevista = agora + timedelta(minutes=minutos)

            timestamp = int(execução_prevista.timestamp())
            tempo_exato = f"<t:{timestamp}:F> (<t:{timestamp}:R>)"

            embed.add_field(name=f"Comando: `{nome_comando}`", value=f"Modo: `{tipo.capitalize()}` (`{tempo}`)\nCanal: {canal_mention}\n Ping: {ping_role}\n Previsto para executar: {tempo_exato}", inline=False)

        await interaction.followup.send(embed=embed)



    





    @app_commands.command(name="setping", description="Configura para mencionar algum ping o comando")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(nome_comando="Escolha o comando que deseja configurar o ping",
                            ping="Escolha o cargo que deseja mencionar no comando")
    async def setping(self, interaction: discord.Interaction, nome_comando: str, ping: discord.Role):

        id_limpo = ping.id if ping else None

        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE automatico SET role_id = ? WHERE guild_id = ? AND nome_comando = ?", (ping.id, interaction.guild.id, nome_comando))
        conn.commit()

        await interaction.followup.send(f"--- Ping configurado com sucesso! ---\n\nComando: `{nome_comando}` | Cargo mencionado: {ping.mention}")




class autoCodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tree.add_command(autocommandsGroup())


    
async def setup(bot):
    await bot.add_cog(autoCodes(bot))