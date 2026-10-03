import discord
from discord.ext import commands
from discord import app_commands
import sqlite3



# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#
#               ADMIN WHITELIST
#
# ------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------



class whitelistGroup(app_commands.Group, name="whitelist", description="Comandos para whitelist aqui"):

    @app_commands.command(name="add", description="Adiciona um cargo ou alguém na whitelist.")
    @app_commands.choices(
        whitelist = [
            app_commands.Choice(name="Cargo específico", value="role"),
            app_commands.Choice(name="Usuário específico", value="user"),
        ]
    )
    @app_commands.describe(whitelist="Escolhe qual tipo irá colocar na whitelist",
                           value="Coloca o cargo ou usuário desejado.")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_whitelist(self, interaction: discord.Interaction, whitelist: str, value: str):

        if interaction.guild is None:
            await interaction.response.send_message("Este comando é somente dedicado para servidores!", ephemeral=True)
        
        id_limpo = value.replace("<@&", "").replace("<@", "").replace(">", "").replace("&", "").replace("!", "").strip()


        if whitelist == "role":

            cargo = interaction.guild.get_role(int(id_limpo)) if id_limpo.isdigit() else None
        

            if cargo.is_default():
                return await interaction.response.send_message(" `❌` Você não pode adicionar o cargo everyone! `❌`", ephemeral=True)

            if not cargo:
                return await interaction.response.send_message("Cargo inexistente ou não encontrado! Certifique-se de usar o ID do cargo ou mencionar", ephemeral=True)
            


            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()

            try:
                cursor.execute('''INSERT OR REPLACE INTO whitelistRole (guild_id, role_id)
                                VALUES (?, ?)''', (interaction.guild.id, cargo.id))
                conn.commit()
                await interaction.response.send_message(f"✔ Cargo `{cargo.name}` adicionado à whitelist com sucesso! ✔", ephemeral=True)
            
            except sqlite3.IntegrityError:
                await interaction.response.send_message(f"❌ O cargo `{cargo.name}` já está na whitelist! ❌", ephemeral=True)
            
            finally:
                conn.close()

        
        elif whitelist == "user":

            usuario = interaction.guild.get_member(int(id_limpo)) if id_limpo.isdigit() else None

            if not usuario:
                return await interaction.response.send_message("Usuário não encontrado.", ephemeral=True)

            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()

            try:
                cursor.execute('''INSERT OR REPLACE INTO whitelistPlayer (guild_id, user_id)
                                    VALUES (?, ?)''', (interaction.guild.id, usuario.id))
                conn.commit()
                await interaction.response.send_message(f"✔ Usuário `{usuario.name}` adicionado à whitelist com sucesso! ✔", ephemeral=True)
            
            except sqlite3.IntegrityError:
                await interaction.response.send_message(f"❌ O usuário `{usuario.name}` já está na whitelist! ❌", ephemeral=True)
            
            finally:
                conn.close()















    @app_commands.command(name="remove", description="Remove um cargo ou alguém da whitelist.")
    @app_commands.choices(
        whitelist = [
            app_commands.Choice(name="Cargo específico", value="role"),
            app_commands.Choice(name="Usuário específico", value="user"),
        ]
    )
    @app_commands.describe(whitelist="Escolhe qual tipo irá remover da whitelist",
                           value="Remove o cargo ou usuário desejado.")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_whitelist(self, interaction: discord.Interaction, whitelist: str, value: str):

        if interaction.guild is None:
            await interaction.response.send_message("Este comando é somente dedicado para servidores!", ephemeral=True)
        
        id_limpo = value.replace("<@&", "").replace("<@", "").replace(">", "").replace("&", "").replace("!", "").strip()


        if whitelist == "role":

            cargo = interaction.guild.get_role(int(id_limpo)) if id_limpo.isdigit() else None

            if cargo.is_default():
                return await interaction.response.send_message(" `❌` Você não pode adicionar o cargo everyone! `❌`", ephemeral=True)

            if not cargo:
                return await interaction.response.send_message("Cargo inexistente ou não encontrado! Certifique-se de usar o ID do cargo ou mencionar", ephemeral=True)
            

            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()

            try:
                cursor.execute('''DELETE FROM whitelistRole WHERE guild_id = ? AND role_id = ?''', (interaction.guild.id, cargo.id))
                conn.commit()
                await interaction.response.send_message(f"✔ Cargo `{cargo.name}` removido da whitelist com sucesso! ✔", ephemeral=True)

            except sqlite3.Error:
                await interaction.response.send_message(f"❌ O cargo `{cargo.name}` não está na whitelist! ❌", ephemeral=True)

            finally:
                conn.close()

        elif whitelist == "user":

            usuario = interaction.guild.get_member(int(id_limpo)) if id_limpo.isdigit else None

            if not usuario:
                return await interaction.message.send_message("Usuário não encontrado.", ephemeral=True)

            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()

            try:
                cursor.execute('''DELETE FROM whitelistPlayer WHERE guild_id = ? AND user_id = ?''', (interaction.guild.id, usuario.id))
                conn.commit()
                await interaction.response.send_message(f"✔ Usuário `{usuario.name}` removido da whitelist com sucesso! ✔", ephemeral=True)

            except sqlite3.Error:
                await interaction.response.send_message(f"❌ O usuário `{usuario.name}` não está na whitelist! ❌", ephemeral=True)

            finally:
                conn.close()















    @app_commands.command(name="list", description="Lista todos os cargos e usuários na whitelist.")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_whitelist(self, interaction: discord.Interaction):

        if interaction.guild is None:
            await interaction.response.send_message("Este comando é somente dedicado para servidores!", ephemeral=True)

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT role_id FROM whitelistRole WHERE guild_id = ?''', (interaction.guild.id,))
        roles = cursor.fetchall()

        cursor.execute('''SELECT user_id FROM whitelistPlayer WHERE guild_id = ?''', (interaction.guild.id,))
        users = cursor.fetchall()

        conn.close()

        embed = discord.Embed(
            title="Whitelist do Servidor",
            description="Aqui estão os cargos e usuários que estão na whitelist deste servidor.",
            color=discord.Color.gold()
        )

        if roles:
            role_mentions = [f"<@&{role_id[0]}>" for role_id in roles]
            embed.add_field(name="Cargos na Whitelist", value="\n".join(role_mentions), inline=False)
        else:
            embed.add_field(name="Cargos na Whitelist", value="Nenhum cargo na whitelist.", inline=False)

        if users:
            user_mentions = [f"<@{user_id[0]}>" for user_id in users]
            embed.add_field(name="Usuários na Whitelist", value="\n".join(user_mentions), inline=False)
        else:
            embed.add_field(name="Usuários na Whitelist", value="Nenhum usuário na whitelist.", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)






class whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.tree.add_command(whitelistGroup())

async def setup(bot):
    await bot.add_cog(whitelist(bot))
    