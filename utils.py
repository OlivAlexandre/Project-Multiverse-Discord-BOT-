import discord
import sqlite3
from discord.ext import commands
from discord import app_commands





def whitelist_adm_slash():
    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.guild is None:
            await interaction.response.send_message("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return False
        
        
        if interaction.user.guild_permissions.administrator:
            return True
        
        try:
            conn = sqlite3.connect("json.db")
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM whitelistPlayer WHERE guild_id = ? AND user_id = ?", 
                            (str(interaction.guild.id), str(interaction.user.id)))

            if cursor.fetchone() is not None:
                return True
        
            user_roles = [str(role.id) for role in interaction.user.roles]
            if user_roles:
                placeholders = ",".join("?" for _ in user_roles)
                query = f"SELECT 1 FROM whitelistRole WHERE guild_id = ? AND role_id IN ({placeholders})"

                cursor.execute(query, [str(interaction.guild.id)] + user_roles)

                if cursor.fetchone() is not None:
                    return True
        finally:
            conn.close()
        erro = "`🚫` Você não tem permissão para usar este comando. `🚫`"
        if not interaction.response.is_done():
            await interaction.response.send_message(erro, ephemeral=True)
        return False

    return app_commands.checks.check(predicate)















def whitelist_adm_prefix():
    async def prediction(ctx: commands.Context) -> bool:
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return False
        
        if ctx.author.guild_permissions.administrator:
            return True
        
        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT 1 FROM whitelistPlayer WHERE guild_id = ? AND user_id = ?", (str(ctx.guild.id), str(ctx.author.id)))


            if cursor.fetchone() is not None:
                return True
            

            author_role = [str(role.id) for role in ctx.author.roles]
            if author_role:
                placeholder = ",".join("?" for _ in author_role)
                query = f"SELECT 1 FROM whitelistRole WHERE guild_id = ? AND role_id IN ({placeholder})"

                cursor.execute(query, [str(ctx.guild.id)] + author_role)

                if cursor.fetchone() is not None:
                    return True
        finally:
            conn.close()
        erro = "`🚫` Você não tem permissão para usar este comando. `🚫`"

        if not ctx.interaction or not ctx.interaction.response.is_done():
            await ctx.send(erro, ephemeral=True)
        return False
    return commands.check(prediction)















class Paginador(discord.ui.View):
    def __init__(self, paginas: list[discord.Embed], timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.paginas = paginas
        self.pagina_atual = 0

        self.atualizar_bots()
    

    def atualizar_bots(self):
        self.voltar.disabled = (self.pagina_atual == 0)
        self.avancar.disabled = (self.pagina_atual == len(self.paginas) - 1)
        self.fim.disabled = (self.pagina_atual == len(self.paginas))
        self.inicio.disabled = (self.pagina_atual == 0)
    

    @discord.ui.button(label="🔰", style=discord.ButtonStyle.red)
    async def inicio(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.pagina_atual = 0
        self.atualizar_bots()
        await interaction.response.edit_message(embed=self.paginas[self.pagina_atual], view=self)

    
    @discord.ui.button(label="◀", style=discord.ButtonStyle.grey)
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.pagina_atual > 0:
            self.pagina_atual -= 1
        
        self.atualizar_bots()
        await interaction.response.edit_message(embed=self.paginas[self.pagina_atual], view=self)

    

    @discord.ui.button(label="▶", style=discord.ButtonStyle.grey)
    async def avancar(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.pagina_atual <len(self.paginas) - 1:
            self.pagina_atual += 1
        
        self.atualizar_bots()
        await interaction.response.edit_message(embed=self.paginas[self.pagina_atual], view=self)

    
    @discord.ui.button(label="🔚", style=discord.ButtonStyle.green)
    async def fim(self, interaction: discord.Interaction, button: discord.ui.Button):

        fim_pag = len(self.paginas)-1
        self.pagina_atual = fim_pag

        self.atualizar_bots()
        await interaction.response.edit_message(embed=self.paginas[self.pagina_atual], view=self)















async def prefixo(bot, message):

    guild = None

    if isinstance(message, discord.Interaction):
        guild = message.guild
    elif hasattr(message, "guild"):
        guild = message.guild
    elif isinstance(message, discord.Guild):
        guild = message



    if not guild:
        return '--'
    
    conn = sqlite3.connect('json.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT prefix FROM bot_config WHERE guild_id = ?''', (guild.id,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0]:
        return resultado[0]

    return '--'















def is_user_whitelisted(interação) -> bool:

    user = interação.user if isinstance(interação, discord.Interaction) else interação.author
    guild = interação.guild

    if not guild or not user:
        return False
    
    if user.id == guild.owner_id:
        return False
    
    if isinstance(user, discord.Member) and user.guild_permissions.administrator:
        return True


    conn = sqlite3.connect("json.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM whitelistPlayer WHERE guild_id = ? AND user_id = ?", (guild.id, user.id))
    result_player = cursor.fetchone() is not None
    conn.close()
    return result_player















def tirar_chances(jsonhere):
    chances = []
    if isinstance(jsonhere, dict):
        chave_chance = next((chave for chave in jsonhere if chave.lower() == "chance"), None)
        if chave_chance is not None:
            try:
                chances.append(float(jsonhere[chave_chance]))
            except ValueError:
                pass
        for valor in jsonhere.values():
            chances.extend(tirar_chances(valor))
    elif isinstance(jsonhere, list):
        for item in jsonhere:
            chances.extend(tirar_chances(item))
    return chances















async def autocomplete_commands(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:

    guild = interaction.guild

    if not guild:
        return []

    conn = sqlite3.connect("json.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT type_archive FROM custom_command WHERE guild_id = ?", (guild.id,))
    tipos_custom = [row[0] for row in cursor.fetchall() if row[0]]

    cursor.execute("SELECT DISTINCT type_archive FROM templates WHERE guild_id = ?", (guild.id,))
    tipos_templates = [row[0] for row in cursor.fetchall() if row[0]]

    conn.close()
    tipos = list(set(tipos_custom + tipos_templates))

    if "todos" not in tipos:
        tipos.append("todos")
    
    opcoes = [
        app_commands.Choice(name=tipo.capitalize(), value=tipo)
        for tipo in tipos
        if current.lower() in tipo.lower()
    ]

    return opcoes[:25]







def busca_molde(guild_id: int, nome_comando: str, tipo_arquivo: str, template: str) -> str:
    if template and template.strip():
        return template
    
    conn = sqlite3.connect('json.db')
    cursor = conn.cursor()

    name_command = (nome_comando or "").lower().strip()
    type_archive = (tipo_arquivo or "").lower().strip()

    cursor.execute('''
            SELECT template_text, 'Comando específico' FROM templates WHERE guild_id = ? AND LOWER(command_name) = ? AND template_text IS NOT NULL AND template_text = ''
            UNION ALL
            SELECT template_text, 'Tipo de arquivo' FROM templates WHERE guild_id = ? AND LOWER(type_archive) = ? AND template_text IS NOT NULL AND template_text = ''
            LIMIT 1
        ''', (guild_id, name_command, guild_id, type_archive))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None