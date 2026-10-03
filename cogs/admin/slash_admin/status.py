import discord
from discord.ext import commands
from discord import app_commands
from utils import whitelist_adm_slash


class statusgroup(app_commands.Group, name="status", description="Comandos para modificar os status do bot."):

    @app_commands.command(name="change", description="[STAFF] Muda os status do bot.")
    @app_commands.choices(
        mudança = [
            app_commands.Choice(name="Jogando", value="playing"),
            app_commands.Choice(name="Assistindo", value="watching"),
            app_commands.Choice(name="Ouvindo", value="listening"),
            app_commands.Choice(name="Streamando", value="stream"),
        ]
    )
    @app_commands.describe(mudança="Escolha qual status o bot terá.", 
                            text="O texto que terá nele",
                            url="Insere a URL do que estiver fazendo (OBS: Apenas para transmissão)")
    @app_commands.checks.has_permissions(administrator=True)
    async def status_change(self, interaction: discord.Interaction, mudança: str, text: str, url: str=None):

        atividade = None
        

        if mudança == "playing":
            atividade = discord.Game(name=text)
        
        elif mudança == "listening":
            atividade = discord.Activity(type=discord.ActivityType.listening, name=text)

        elif mudança == "watching":
            atividade = discord.Activity(type=discord.ActivityType.watching, name=text)

        elif mudança == "stream":
            if not url or not (url.startwith("https://www.twitch.tv/") or url.startwitch("https://www.youtube.com")):
                return await interaction.response.send_message("Insira uma URL válida da Twitch ou do youtube mostrando estar em Stream!", ephemeral=True)

            atividade = discord.Streaming(name=text, url=url)

        await interaction.client.change_presence(activity=atividade)

        mensagem = f"Status alterado para `{mudança.capitalize()} {text}`"
        if url and mudança == "stream":
            mensagem += f"Link da transmissão: <{url}>"
        
        await interaction.response.send_message(mensagem, ephemeral=True)





class statusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.tree.add_command(statusgroup())


async def setup(bot):
    await bot.add_cog(statusCog(bot))