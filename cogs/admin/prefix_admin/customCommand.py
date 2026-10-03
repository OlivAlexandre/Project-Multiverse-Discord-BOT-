import discord
from discord.ext import commands
import json
import io
import sqlite3
from utils import prefixo, whitelist_adm_prefix, tirar_chances


class CustomCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    
# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#
#    CUSTOM COMMANDS (ADMIN VERSION)
#
# ------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------





    @commands.group(name="customcommand", invoke_without_command=True)
    @whitelist_adm_prefix()
    async def customC_group(self, ctx):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return
        
        await ctx.send(f"Especifique a ação do JSON: Use `{prefixo_prefix}customcommand [upload/list/download/delete]`")











    @customC_group.command(name="list")
    @whitelist_adm_prefix()
    async def list_json_prefix(self, ctx):
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.")
            return

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT command_name, type_command, type_archive FROM custom_command WHERE guild_id = ?''',
                       (int(ctx.guild.id),))
        comandos = cursor.fetchall()
        conn.close()

        if not comandos:
            await ctx.send("Nenhum comando customizado encontrado para este servidor.")
            return
        
        embed = discord.Embed(
            title="Comandos Customizados do Servidor",
            description="Lista de comandos customizados criados para este servidor.",
            color=discord.Color.purple()
        )
        for nome_cmd, tipo_cmd, tipo_archive in comandos:
            embed.add_field(name=nome_cmd, value=f"Tipo específico: {tipo_cmd}\n\nTipo padrão: {tipo_archive}", inline=False)
        
        await ctx.send(embed=embed)









    
    @customC_group.command(name="delete")
    @whitelist_adm_prefix()
    async def delete_json_prefix(self, ctx, *, nome_comando: str):
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.")
            return

        nome_cmd = nome_comando.lower().strip()

        if nome_cmd is None:
            prefixo_prefix = await prefixo(self.bot, ctx.message)
            await ctx.send(f"Por favor, forneça o nome do comando que deseja deletar. Exemplo: `{prefixo_prefix}customcommand delete <nome_do_comando>`")
            return

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (int(ctx.guild.id), nome_cmd))
        afetado = cursor.rowcount
        conn.commit()
        conn.close()
        if rows_afetados := afetado:
            await ctx.send(f"Comando `{nome_cmd}` excluído com sucesso! ({rows_afetados} linha(s) afetada(s))")
        else:
            await ctx.send(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.")
    









    @customC_group.command(name="download")
    @whitelist_adm_prefix()
    async def download_json_prefix(self, ctx, *, nome_comando: str):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.")
            return

        nome_cmd = nome_comando.lower().strip()

        if nome_cmd is None:
            await ctx.send(f"Por favor, forneça o nome do comando que deseja baixar. Exemplo: `{prefixo_prefix}customcommand download <nome_do_comando>`")
            return

        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT json_data FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (int(ctx.guild.id), nome_cmd))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            await ctx.send(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.")
            return
        
        json_formatado = json.dumps(json.loads(resultado[0]), indent=2, ensure_ascii=False)

        arquivo = io.BytesIO(json_formatado.encode('utf-8'))
        dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")
        await ctx.send(f"Arquivo JSON do comando `{nome_cmd}`:", file=dc_file)
    









    @customC_group.command(name="upload")
    @whitelist_adm_prefix()
    async def upload_json_prefix(self, ctx, json_file: discord.Attachment):
        arquivo = json_file or (ctx.message.attachments[0] if ctx.message.attachments else None)

        if not arquivo:
            return await ctx.send("Por favor, envie um arquivo JSON como anexo ou forneça o link do arquivo.")

        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.")
            return

        if not arquivo.filename.endswith('.json'):
            return await ctx.send("Por favor, envie um arquivo com extensão .json.")


        await ctx.send("Processando o arquivo JSON...")

        try:
            file_bytes = await arquivo.read()
            print("Lendo arquivos...")
            json_data = json.loads(file_bytes.decode('utf-8'))

            campos_obrigatorios = ["nome_comando", "tipo_comando", "tipo_arquivo"]
            print("Checando se possui...")
            if not all(campo in json_data for campo in campos_obrigatorios):
                return await ctx.send("O arquivo JSON deve conter os seguintes campos: `nome_comando`, `tipo_comando` e `tipo_arquivo`.")
            
            nome_cmd = json_data["nome_comando"].lower().strip()
            tipo_cmd = json_data["tipo_comando"].lower().strip()
            tipo_arquivo = json_data["tipo_arquivo"].lower().strip()
            type = json_data.get("type", "")
            print("Colocando umas partes em variável...")

            if tipo_cmd == "random":
                lista_chances = tirar_chances(json_data)
                print("É random?")

                if type is None:
                                    return await ctx.send("Ops... houve um erro, você retirou algo do JSON universal, mantenha novamente.")

                if not lista_chances:
                    return await ctx.send("Não há nenhum campo com 'chance' no arquivo.")

                soma = sum(lista_chances)

                if not (99.9999 <= soma <= 100.0001):
                    return await ctx.send("A soma das chances dos itens deve ser igual a 100%.")
                                
            
            


            print("Passou no teste e está indo para o banco de dados.")
            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT OR REPLACE INTO custom_command (guild_id, command_name, type_command, type_archive, type, json_data)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (ctx.guild.id, nome_cmd.lower(), tipo_cmd, tipo_arquivo, type, json.dumps(json_data, ensure_ascii=False)))
            conn.commit()
            print(f"[DEBUG] Colocado o comando com nome de {nome_cmd}")
            conn.close()
            await ctx.send(f"Comando `{nome_cmd}` do tipo `{tipo_arquivo} | {tipo_cmd}` criado/atualizado com sucesso!")
        except json.JSONDecodeError:
            await ctx.send("O arquivo enviado não é um JSON válido. Por favor, verifique o conteúdo do arquivo.")
        except Exception as e:
            print(f"Erro ao processar o arquivo JSON: {e}")
            await ctx.send("Ocorreu um erro ao processar o arquivo. Por favor, tente novamente.")
    













    @customC_group.command(name="add")
    @whitelist_adm_prefix()
    async def add_category(self, ctx, nome_comando: str, quantidade: int):
        if ctx.guild is None:
            await ctx.send("Este comando não pode ser usado em mensagens diretas.")
            return

        nome_cmd = nome_comando.lower().strip()
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT json_data FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (ctx.guild_id, nome_cmd))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            await ctx.send(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.")
            return

        json_data = json.loads(resultado[0])

        if json_data["tipo_arquivo"] == "mineração":

            if "config_random" not in json_data or "itens" not in json_data["config_random"]:
                await ctx.send("O JSON do comando não está no formato esperado para mineração.")
                return

            for i in range(quantidade):
                json_data["config_random"]["itens"].append(
                    {
                        "nome": "Item", 
                        "raridade": "Comum/Incomum/Raro/Super Raro/Épico/Místico/Lendário", 
                        "chance": 999.999, 
                        "nivel_picareta": "nível", 
                        "curiosidade": "Curiosidade do item", 
                        "imagem": "https://link.com/item.png"
                    }
                )

            arquivo = io.BytesIO(json.dumps(json_data, ensure_ascii=False, indent=4).encode('utf-8'))
            dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")

            await ctx.reply(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)



        elif json_data["tipo_arquivo"] == "universal":

            if "itens" not in json_data:
                await ctx.send("O JSON do comando não está no formato esperado para o comando Universal.")
                return

            for i in range(quantidade):
                json_data["itens"].append(

                    {"emoji_item": "",
                        "name": "",
                        "sufixo": "",
                        "chance": 999.999,
                    "text1": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "text2": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "text3": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "text4": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "text5": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "text6": {
                        "type": "(alguma coisa, raridade, tipo do item...)",
                        "emoji": "(emoji que queira colocar no seu type)",
                        "line1": "",
                        "line2": "",
                        "line3": "",
                        "line4": "",
                        "line5": "",
                        "line6": "",
                        "line7": "",
                        "line8": "",
                        "line9": "",
                        "line10": "",
                        "line11": "",
                        "line12": "",
                        "line13": ""
                        },
                    "imagem": "https://link.com/item.png" },

                )

            arquivo = io.BytesIO(json.dumps(json_data, ensure_ascii=False, indent=4).encode('utf-8'))
            dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")
            await ctx.reply(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)
        

        elif json_data["tipo_arquivo"] == "loja":

            if "itens" not in json_data:
                await ctx.send("O JSON do comando não está no formato esperado para loja.")
                return

            for i in range(1, quantidade + 1):
                json_data["itens"].append(

                    {"id": f"{i} (pode trocar para o nome do próprio ou deixar número)",
                        "nome": "(Nome do item)",
                        "valor": 0,
                        "moeda": "yene/real/dolar",
                        "descricao": "(descrição do item)",
                        "status":{
                            "hp": "X0",
                            "forca": "X0",
                            "energia": "X0",
                            "vigor": "X0",
                            "velocidade": "X0",
                        },
                        "curiosidade": "(curiosidade do item)",
                        "rank": "(rank do item)",
                        "imagem": "link"
                        },
                                    
                )

            arquivo = io.BytesIO(json.dumps(json_data, ensure_ascii=False, indent=4).encode('utf-8'))
            dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")
            await ctx.reply(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)

        elif json_data["tipo_arquivo"] == "procurado":

            if "itens" not in json_data:
                await ctx.send("O JSON do comando não está no formato esperado para procurados.")
                return

            for i in range(quantidade):
                json_data["itens"].append(

                    {"id": f"{i} (pode trocar para o nome do próprio ou deixar número)",
                        "nome": "(Nome do procurado)",
                        "recompensa": "(recompensa ao conseguir)",
                        "descricao": "(descrição do procurado)",
                        "nivel_procurado": "F/E/D/C/B/A/S/SS",
                        "imagem": "link/imagem do procurado"},
                                    
                )

            arquivo = io.BytesIO(json.dumps(json_data, ensure_ascii=False, indent=4).encode('utf-8'))
            dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")
            await ctx.reply(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)






async def setup(bot):
    await bot.add_cog(CustomCommand(bot))