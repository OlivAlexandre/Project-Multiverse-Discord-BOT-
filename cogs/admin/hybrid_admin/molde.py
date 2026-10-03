import discord
from discord.ext import commands
from discord import app_commands
import json
import io
import sqlite3
from utils import whitelist_adm_prefix, prefixo, Paginador, autocomplete_commands


class MoldeCustomC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="molde", description="Comandos relacionado aos moldes", invoke_without_command=True)
    @whitelist_adm_prefix()
    async def moldeC_group(self, ctx: commands.Context):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return

        await ctx.send(f"Especifique a ação do molde: Use `{prefixo_prefix}molde [set/view/delete]`")















    @moldeC_group.command(name="set", description="[STAFF] Define um molde para o comando customizado (OBS: Use versão de prefixo).")
    @app_commands.describe(tipo_comando="Escolha o tipo de comando customizado que deseja configurar o molde", 
                           texto_molde="Digite o texto do molde que deseja configurar")
    @whitelist_adm_prefix()
    @app_commands.autocomplete(tipo_comando=autocomplete_commands)
    async def set_molde_command(self, ctx: commands.Context, tipo_comando: str, *, texto_molde: str = None):
        
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return
        
        if not texto_molde:
            return await ctx.send("Ops! Não há molde para ser usado...")

        tipo_cmd = tipo_comando.lower().strip()

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("SELECT command_name FROM custom_command WHERE guild_id = ? AND LOWER(command_name) = ?", (ctx.guild.id, tipo_cmd))
        cmd_row = cursor.fetchone()

        if cmd_row:
            cursor.execute("UPDATE custom_command SET template_text = ? WHERE guild_id = ? AND LOWER(command_name) = ?", (texto_molde, ctx.guild.id, tipo_cmd))
            cursor.execute('''
                            INSERT OR REPLACE INTO templates (guild_id, command_name, template_text) VALUES (?, ?, ?)''',
                           (ctx.guild.id, tipo_cmd, texto_molde)
            )
            conn.commit()
            conn.close()
            return await ctx.send(f"Modelo ***específico*** para o comando `{tipo_cmd}` definido com sucesso!")


        cursor.execute("SELECT DISTINCT type_archive FROM custom_command WHERE guild_id = ? AND LOWER(type_archive) = ?",
                       (ctx.guild.id, tipo_cmd))
        type_archive_row = cursor.fetchone()


        if type_archive_row:
            cursor.execute('''
                            INSERT OR REPLACE INTO templates (guild_id, type_archive, templates) VALUES (?, ?, ?)''',
                            (ctx.guild.id, tipo_cmd, texto_molde))
            conn.commit()
            conn.close()
            return await ctx.sen(f"Modelo para o tipo arquivado `{tipo_cmd}` definido com sucesso!")

        
        conn.close()
        return await ctx.send(f"O identificador `{tipo_cmd}` não foi encontrado em local algum...")
    













    
    @moldeC_group.command(name="view", description="[STAFF] Vê qual molde está usando em específico")
    @app_commands.autocomplete(tipo_comando=autocomplete_commands)
    @app_commands.describe(tipo_comando="Escolha o tipo de comando customizado que deseja visualizar o molde (entre os 3 tipos ou todos)")
    @whitelist_adm_prefix()
    @app_commands.checks.has_permissions(administrator=True)
    async def view_molde_command(self, ctx: commands.Context, tipo_comando: str):
        
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        tipo_cmd = tipo_comando.lower().strip()
        if tipo_cmd == "todos":
            cursor.execute("SELECT command_name, type_archive, templates WHERE guild_id = ?", (ctx.guild.id,))
            all_moldes = cursor.fetchall()
            conn.close()

            if not all_moldes:
                return await ctx.send("Não há moldes definidos em local algum para nenhum comando.")

            embed = discord.Embed(
                title="Modelos cadastrados",
                color=discord.Color.dark_green()
            )
            for command_name, type_archive, templates in all_moldes:
                identifier = command_name or type_archive or "Desconhecido"
                embed.add_field(name=f"Alvo: `{identifier}`", value=f"```\n{templates[:500]}\n```", inline=False)

            return await ctx.send(embed=embed)
        

        cursor.execute('''
            SELECT template_text, 'Comando específico' FROM templates WHERE guild_id = ? AND LOWER(command_name) = ?
            UNION ALL
            SELECT template_text, 'Tipo de arquivo' FROM templates WHERE guild_id = ? AND LOWER(type_archive) = ?
            LIMIT 1
        ''', (ctx.guild.id, tipo_cmd, ctx.guild.id, tipo_cmd))

        result = cursor.fetchone()

        if not result:
            cursor.execute("SELECT template FROM custom_command WHERE guild_id = ? AND LOWER(command_name) AND template IS NOT NULL", 
                            (ctx.guild.id, tipo_cmd))
            custom_res = cursor.fetchone()
            if custom_res and custom_res[0]:
                resultado = (custom_res[0], 'Comando customizado (Atributo)')

        conn.close()

        if resultado and resultado[0]:

            embed = discord.Embed(
                title=f"Modelo para `{tipo_cmd}`",
                description=f"***Nível:*** {resultado[1]}\n\n```\n{resultado[0]}\n```",
                color=discord.Color.dark_blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Não há modelo específico ou global definido para {tipo_cmd}")


    












    @moldeC_group.command(name="help", description="[STAFF] Exibe exemplos de modelos para os tipos de comando customizado.")
    @whitelist_adm_prefix()
    @app_commands.checks.has_permissions(administrator=True)
    async def help_molde_command(self, ctx: commands.Context):

        embed = discord.Embed(
            title="Modelos de padrão de moldes",
            description="Modelos para colocar no seu molde para o bot reconhecer o que deve ser trocado\n(OBS: Use os literais como vê, se vê `[nome]`, coloque o literal ''[nome]''.).",
            color=discord.Color.blue()
        )

        embed.add_field(name="Substituição de nome", value="Use:\n- `[nome]`\n- `[nome do item]`\n- `[nome item]`\n\n- Para substituir pelo nome do item que foi sorteado.", inline=False)
        embed.add_field(name="Substituição de nível de picareta", value="Use:\n- `[nivel da picareta]`\n- `[nivel de picareta]`\n- `[nivel picareta]`\n\n- Para substituir pelo nível da picareta necessária para minerar tal minério.", inline=False)
        embed.add_field(name="Substituição de chance", value="Use:\n- `[chance]`\n- `[porcentagem]`\n- `[raridade]`\n\n- Para substituir pela chance de cair o item sorteado.", inline=False)
        embed.add_field(name="Substituição de imagem", value="Use:\n- `[imagem]`\n- `[imagem do item]`\n- `[link]`\n\n- Para substituir pela imagem do item sorteado.", inline=False)
        embed.set_footer(text="Troque o que for no molde pelo que está acima para substituir de acordo com o inserido, seja lá item, chance, imagem, nível, etc.")
        embed.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)

        embed2 = discord.Embed(
            title="Modelos de Comandos Customizados - (página 2)",
            description="Exemplos de modelos para os tipos de comando `daily`.",
            color=discord.Color.blue()
        )
        
        embed2.add_field(name="Substituição de valor", value="Use:\n- `[premiado]`\n- `[nome do item]`\n- `[item]`\n- `[ganho]`\n\n- Para substituir pelo valor do prêmio diário sorteado.", inline=False)
        embed2.add_field(name="Substituição de sufixo", value="Use:\n- `[sufixo]`\n- `[frase final]`\n- `[final]`\n\n- Para substituir pelo sufixo do item sorteado.", inline=False)
        embed2.add_field(name="Substituição de chance", value="Use:\n- `[chance]`\n- `[porcentagem]`\n- `[raridade]`\n\n- Para substituir pela chance de cair o item sorteado.", inline=False)
        embed2.add_field(name="Substituição de imagem/GIF", value="Use:\n- `[imagem]`\n- `[gif]`\n- `[link]`\n\n- Para substituir pela imagem ou GIF que havia setado.", inline=False)
        embed2.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)


        embed3 = discord.Embed(
            title="Modelos de Comandos Customizados - (página 3)",
            description="Exemplos de modelos para os tipos de comando `clima`.",
            color=discord.Color.blue()
        )
        embed3.add_field(name="Substituição de clima", value="Use:\n- `[frase]`\n- `[fala]`\n\n- Para substituir por uma frase na qual queira colocar para o clima.", inline=False)
        embed3.add_field(name="Substituição de temperatura", value="Use:\n- `[temperatura]`\n- `[temp]`\n- `[temp.]`\n\n- Para substituir pela temperatura que foi sorteada.", inline=False)
        embed3.add_field(name="Substituição de emojis dos climas", value="Use:\n`[emoji]`\n- (Para emojis setados dos climas)\n\n[emoji do clima]\n[emoji do dia]\n[emoji da hora]\n- (Para emojis setados do dia/tarde/noite...)", inline=False)
        embed3.add_field(name="Forma de colocar ''do dia/da noite''", value="Use:\n- `[dia/noite]`\n- `[do dia/noite]`\n- `[do clima]`\n\n- Para substituir algo para facilitar em colocar ''do dia/tarde/noite''", inline=False)
        embed3.add_field(name="Substituição de imagem/GIF", value="Use:\n- `[imagem]`\n- `[gif]`\n- `[link]`\n\n- Para substituir pela imagem ou GIF que havia setado.", inline=False)
        embed3.add_field(name="Para efeitos dos climas", value="Use:\n- `[ganhos]\n- `[efeito]`\n\n- Para substituir pelo efeito que o clima dá, seja ele positivo ou negativo.", inline=False)
        embed3.add_field(name="Para menção de algum cargo caso coloque", value="Use:\n- `[ping]`\n- `[cargo]`\n- `[menção]`\n\n- Para substituir pela menção de algum cargo que tenha colocado para o clima.", inline=False)
        embed3.add_field(name="Para adicionar curiosidades do clima", value="Use:\n- `[curiosidade]`\n\n- Para adicionar uma curiosidade de tal clima no seu molde.")
        embed3.set_image(url=ctx.guild.icon.url if ctx.guild.icon else None)


        lista = [embed, embed2, embed3]
        view=Paginador(paginas=lista)

        await ctx.reply(embed=lista[0], view=view)














    @moldeC_group.command(name="delete", description="[STAFF] Deleta o molde usado.")
    @whitelist_adm_prefix()
    @app_commands.autocomplete(tipo_comando=autocomplete_commands)
    @app_commands.describe(tipo_comando="Escolha o tipo de comando customizado que deseja deletar o molde (entre os 3 tipos ou todos)")
    async def delete_molde_command(self, ctx: commands.Context, tipo_comando: str):

        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return
        
        tipo_cmd = tipo_comando.lower().strip()

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()

        cursor.execute("""
                        DELETE FROM templates
                        WHERE guild_id = ? AND (LOWER(command_name) = ? OR LOWER(type_archive) = ?)""",
                        (ctx.guild.id, tipo_cmd, tipo_cmd))

        deletados = cursor.rowcount

        cursor.execute("""
                        UPDATE custom_command
                        SET template = NULL
                        WHERE guild_id = ? and LOWER(command_name) = ?""",
                    (ctx.guild.id, tipo_cmd))

        deletados_custom = cursor.rowcount

        conn.commit()
        conn.close()

        if deletados > 0 or deletados_custom > 0:
            await ctx.send(f"O odelo para `{tipo_cmd}` foi removido con sucesso!!")
        else:
            await ctx.send(f"Nenhum modelo foi encontrado para o `{tipo_cmd}`")






async def setup(bot):
    await bot.add_cog(MoldeCustomC(bot))