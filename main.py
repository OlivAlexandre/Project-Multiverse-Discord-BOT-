import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import sqlite3


load_dotenv()
multiToken = os.getenv('multiToken')

async def prefixo(bot, message):
    if not message.guild:
        return '--'
    
    conn = sqlite3.connect('json.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT prefix FROM bot_config WHERE guild_id = ?''', (str(message.guild.id),))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else '--'

class MultiBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=prefixo,
            intents=discord.Intents.all()
        )
        self.synced = False
        self.remove_command("help")
        

    async def setup_hook(self):
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS custom_command (
                            guild_id INTEGER,
                            command_name TEXT,
                            type_command TEXT,
                            type_archive TEXT,
                            type VARCHAR(30),
                            json_data TEXT,
                            template_text TEXT,
                            PRIMARY KEY (guild_id, command_name)
                         )''')
                         
        cursor.execute('''CREATE TABLE IF NOT EXISTS templates (
                            guild_id INTEGER,
                            type_command TEXT,
                            type_archive TEXT,
                            template_text TEXT,
                            PRIMARY KEY (guild_id, type_command)
                         )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS bot_config (
                            guild_id INTEGER PRIMARY KEY,
                            prefix TEXT DEFAULT '--'
                         )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS whitelistPlayer (
                            guild_id INTEGER PRIMARY KEY,
                            user_id INTEGER
                            )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS whitelistRole (
                            guild_id INTEGER PRIMARY KEY,
                            role_id INTEGER
                            )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS automatico (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            guild_id INTEGER,
                            canal_id INTEGER,
                            role_id INTEGER,
                            nome_comando TEXT,
                            tipo TEXT,
                            tempo TEXT,
                            ultima_execucao TEXT,
                            UNIQUE (guild_id, nome_comando)
                            )''')
        
        #cursor.execute("ALTER TABLE custom_command ADD COLUMN type VARCHAR(30)")
        #cursor.execute("ALTER TABLE templates ADD COLUMN command_name TEXT")
        conn.commit()
        conn.close()

        for caminho_atual, pastas, arquivos in os.walk("./cogs"):
            for arquivo in arquivos:
                if arquivo.endswith(".py"):
                    caminho_livre = caminho_atual.replace("./", "").replace("/", ".").replace("\\", ".")
                    nome_extensao = f"{caminho_livre}.{arquivo[:-3]}"

                    try:
                        await self.load_extension(nome_extensao)
                        print(f"Extensão {nome_extensao} carregada com sucesso!\n")
                    except Exception as e:
                        print(f"Erro ao carregar a extensão {nome_extensao}: {e}\nLinha {e.__traceback__.tb_lineno}\n")
        await self.tree.sync()
                

    async def on_ready(self):
        print(f'{self.user} logado com sucesso!!')

        if not self.synced:
            try:
                await self.tree.sync()
                self.synced = True
                print("Comandos slash conectado com sucesso.")
            except Exception as e:
                print(f"Erro de conexão com comandos slash: {e}")
        

        await self.tree.sync()
    
bot = MultiBot()

#@bot.event
#async def on_command_error(ctx: commands.Context, error: commands.CommandError):
#    
#
#   if isinstance(error, commands.CommandNotFound):
#
#        if ctx.guild is None:
#            return
#        
#        comando_digitado = ctx.invoked_with
#
#        conn = sqlite3.connect('json.db')
#        cursor = conn.cursor()
#        cursor.execute("SELECT 1 FROM custom_command WHERE guild_id = ? and LOWER(command_name) = LOWER(?)", 
#                       (int(ctx.guild.id), comando_digitado))
#       custom_commands = cursor.fetchone()
#       conn.close()
#
#       if custom_commands:
#            return
#
#       prefixo_prefix = await prefixo(bot, ctx.message)
#       await ctx.reply(
#           f"Sinto muito! Mas o comando `{prefixo_prefix}{comando_digitado}` não existe!\n"
#           f"[ADMIN] Digite `{prefixo_prefix}helpall` para ver a lista de comandos disponíveis!\n"
#           f"[PLAYER] Digite `{prefixo_prefix}helpbot` para ver a lista de comandos disponíveis!",
#           delete_after=10
#       )
#       return
#   print(f"Erro no comando: {error}")






@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandInvokeError) and isinstance(error.original, commands.CommandNotFound):
        await interaction.followup.send("Sinto muito! Este comando ou subcomando não foi encontrado ou está desativado!", ephemeral=True)
        return

    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.followup.send("Ops! Você não tem permissão para mexer nesse comando!", ephemeral=True)
        return
    
    if interaction.response.is_done():
        await interaction.followup.send("Ocorreu um erro interno ao executar este comando...", ephemeral=True)
    
    try:
        await interaction.followup.send("Erro interno ao executar este comando...", ephemeral=True)
    except discord.NotFound:
        pass
    print(f"Erro em slash command: {error}")






@bot.event
async def on_message(message):
    prefixo_prefix = await prefixo(bot, message)
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        if not message.content.startswith(f"<@{bot.user.id}>") and not message.content.startswith(f"<@!{bot.user.id}>"):
            return
        ctx = await bot.get_context(message)
        if not ctx.valid:
            await message.reply(f"Olá {message.author.mention}! O meu prefixo é {prefixo_prefix}, use `{prefixo_prefix}helpbot` para ver meus comandos")
            return

    await bot.process_commands(message)






bot.run(multiToken)