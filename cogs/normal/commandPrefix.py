import discord
from discord.ext import commands
import sqlite3
from utils import Paginador, prefixo


class CommandPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    



    
    @commands.command(name="helpbot")
    async def helpPrefix(self, ctx):
        prefixos = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
             await ctx.send("Este comando não pode ser usado em mensagens diretas.")
             return
        
        embed = discord.Embed(
            title="Help - Uso do Prefixo",
            description=f"Lista de comandos disponíveis com o prefixo `{prefixos}` (comandos livres)",
            color=discord.Color.green()
        )
        if ctx.guild.icon:
            embed.set_image(url=ctx.guild.icon.url)
        else:
            embed.set_image(url=ctx.bot.user.avatar.url)

        embed.add_field(name=f"`{prefixos}teste`", value="Verifica se o bot está funcionando corretamente.", inline=False)
        embed.add_field(name=f"`{prefixos}donate`", value="Mostra informações sobre como apoiar o criador do bot.", inline=False)


        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute("SELECT command_name, type_command, type_archive FROM custom_command WHERE guild_id = ?", (int(ctx.guild.id),))
        custom_commands = cursor.fetchall()

        if not custom_commands:
            await ctx.reply(embed=embed)
            return

        embed_custom = discord.Embed(
            title="Comandos Personalizados",
            description="Aqui você verá todos os comandos personalizados disponíveis neste servidor.",
            color=discord.Color.blue()
        )

        for nome_comando, tipo_comando, tipo_arquivo in custom_commands:
            embed_custom.add_field(name=f"`{prefixos}{nome_comando}`", 
                                   value=f"Tipo do comando: {tipo_arquivo}", inline=False)
            
        lista = [embed, embed_custom]
        view = Paginador(paginas=lista)
        await ctx.reply(embed=lista[0], view=view)















    @commands.command(name="teste")
    async def test(self, ctx):
        await ctx.send("# `Bot funcionando corretamente!`")















    @commands.command(name="donate")
    async def donate(self, ctx):
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
        await ctx.send(embed=embed)















    @commands.command(name="prefixo")
    async def prefixBot(self, ctx):

        if ctx.guild is None:
            await ctx.send("O prefixo padrão do bot é `--`")
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT prefix FROM bot_config WHERE guild_id = ?", (ctx.guild.id,))
        result = cursor.fetchone()

        if result is None:

            cursor.execute("UPDATE bot_config SET prefix = ? WHERE guild_id = ?", ("--", ctx.guild.id))
            conn.commit()

            return await ctx.send("Nenhum prefixo personalizado encontrado para este servidor. O prefixo padrão `--` foi definido.")
        else:
            prefix = result[0]
            return await ctx.send(f"O prefixo personalizado deste servidor é: `{prefix}`")
    














    
    
    

    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latência: {self.bot.latency * 1000:.2f} ms")




    
    
async def setup(bot):
    await bot.add_cog(CommandPrefix(bot))
