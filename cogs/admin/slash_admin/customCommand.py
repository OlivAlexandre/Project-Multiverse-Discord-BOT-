import discord
from discord.ext import commands
from discord import app_commands
import json
import io
import sqlite3
from utils import tirar_chances, whitelist_adm_slash








# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
#
#               CUSTOM COMMAND (ADMIN VERSION)
#
# ------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------




class JsonGroup(app_commands.Group, name="customcommand", description="Comandos Admin para os Custom Commands."):
    


    @app_commands.command(name="upload", description="[STAFF] Adiciona um comando customizado em JSON.")
    @whitelist_adm_slash()
    async def upload_json(self, interaction: discord.Interaction, json_file: discord.Attachment):

        arquivo = json_file or (interaction.message.attachments[0] if interaction.message.attachments else None)
        
        if not arquivo:
            return await interaction.followup.send("Por favor, envie um arquivo JSON como anexo ou forneça o link do arquivo.")

        if interaction.guild is None:
            await interaction.followup.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return

        if not arquivo.filename.endswith('.json'):
            return await interaction.followup.send("Por favor, envie um arquivo com extensão .json.", ephemeral=True)


        await interaction.response.send_message("Processando o arquivo JSON...")

        try:
            file_bytes = await arquivo.read()
            print(f"[DEBUG] Lendo arquivo JSON: {arquivo.filename}")
            json_data = json.loads(file_bytes.decode('utf-8'), strict=False)

            campos_obrigatorios = ["nome_comando", "tipo_comando", "tipo_arquivo"]
            print("Checando se possui...")
            if not all(campo in json_data for campo in campos_obrigatorios):
                return await interaction.followup.send("O arquivo JSON deve conter os seguintes campos: `nome_comando`, `tipo_comando` e `tipo_arquivo`.", ephemeral=True)
            
            nome_cmd = json_data["nome_comando"].lower().strip()
            tipo_cmd = json_data["tipo_comando"].lower().strip()
            tipo_arquivo = json_data["tipo_arquivo"].lower().strip()
            type = json_data.get("type", "")
            

            if tipo_cmd == "random":
                
                if type is None:
                    return await interaction.followup.send("Ops... houve um erro, você retirou algo do JSON universal, mantenha novamente.", ephemeral=True)

                lista_chances = tirar_chances(json_data)
                print("É random?")

                if not lista_chances:
                    return await interaction.followup.send("Não há nenhum campo com 'chance' no arquivo.", ephemeral=True)

                soma = sum(lista_chances)

                if not (99.9999 <= soma <= 100.0001):
                    return await interaction.followup.send("A soma das chances dos itens deve ser igual a 100%.", ephemeral=True)
            


                
            conn = sqlite3.connect('json.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT OR REPLACE INTO custom_command (guild_id, command_name, type_command, type_archive, type, json_data)
                              VALUES (?, ?, ?, ?, ?)''',
                           (int(interaction.guild_id), nome_cmd.lower(), tipo_cmd, tipo_arquivo, type, json.dumps(json_data, ensure_ascii=False)))
            conn.commit()
            print(f"[DEBUG] Colocado o comando com nome de {nome_cmd}")
            conn.close()

            
            await interaction.followup.send(f"Comando `{nome_cmd}` do tipo `{tipo_arquivo} | {tipo_cmd}` criado/atualizado com sucesso!", ephemeral=True)
        except json.JSONDecodeError:
            await interaction.followup.send("O arquivo enviado não é um JSON válido. Por favor, verifique o conteúdo do arquivo.", ephemeral=True)
        except Exception as e:
            print(f"Erro ao processar o arquivo JSON: {e}")
            await interaction.followup.send("Ocorreu um erro ao processar o arquivo. Por favor, tente novamente.", ephemeral=True)















    @app_commands.command(name="delete", description="[STAFF] Deleta um comando customizado")
    @whitelist_adm_slash()
    async def delete_json(self, interaction: discord.Interaction, nome_comando: str):
        
        if interaction.guild is None:
            await interaction.response.send_message("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return
        
        nome_cmd = nome_comando.lower().strip()
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (int(interaction.guild_id), nome_cmd))
        afetado = cursor.rowcount
        conn.commit()
        conn.close()
        if rows_afetados := afetado:
            await interaction.response.send_message(f"Comando `{nome_cmd}` excluído com sucesso! ({rows_afetados} linha(s) afetada(s))", ephemeral=True)
        else:
            await interaction.response.send_message(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.", ephemeral=True)















    @app_commands.command(name="list", description="[STAFF] Lista os comandos customizados do servidor")
    @whitelist_adm_slash()
    async def list_json(self, interaction: discord.Interaction):
        if interaction.guild is None:
            await interaction.response.send_message("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return
        
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT command_name, type_command, type_archive FROM custom_command WHERE guild_id = ?''',
                       (int(interaction.guild_id),))
        comandos = cursor.fetchall()
        conn.close()

        if not comandos:
            await interaction.response.send_message("Nenhum comando customizado encontrado para este servidor.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="Comandos Customizados do Servidor",
            description="Lista de comandos customizados criados para este servidor.",
            color=discord.Color.purple()
        )
        for nome_cmd, tipo_cmd, tipo_arquivo in comandos:
            embed.add_field(name=nome_cmd, value=f"Tipo: {tipo_cmd}\nTipo de Arquivo: {tipo_arquivo}", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)















    @app_commands.command(name="download", description="[STAFF] Baixa o arquivo JSON de um comando customizado")
    @whitelist_adm_slash()
    async def download_json(self, interaction: discord.Interaction, nome_comando: str):
        if interaction.guild is None:
            await interaction.response.send_message("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return

        nome_cmd = nome_comando.lower().strip()
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT json_data FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (interaction.guild_id, nome_cmd))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            await interaction.response.send_message(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.", ephemeral=True)
            return
        
        json_formatado = json.dumps(json.loads(resultado[0]), indent=2, ensure_ascii=False)

        arquivo = io.BytesIO(json_formatado.encode('utf-8'))
        dc_file = discord.File(fp=arquivo, filename=f"{nome_cmd}.json")
        await interaction.response.send_message(f"Arquivo JSON do comando `{nome_cmd}`:", file=dc_file, ephemeral=True)


    











    @app_commands.command(name="add", description="Adiciona mais categorias a um comando customizado existente.")
    @whitelist_adm_slash()
    async def add_category(self, interaction: discord.Interaction, nome_comando: str, quantidade: int):
        await interaction.response.defer(ephemeral=True)


        if interaction.guild is None:
            await interaction.followup.send("Este comando não pode ser usado em mensagens diretas.", ephemeral=True)
            return

        nome_cmd = nome_comando.lower().strip()
        conn = sqlite3.connect('json.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT json_data FROM custom_command WHERE guild_id = ? AND command_name = ?''',
                       (interaction.guild_id, nome_cmd))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            await interaction.followup.send(f"Comando `{nome_cmd}` não encontrado. Verifique o nome e tente novamente.", ephemeral=True)
            return

        json_data = json.loads(resultado[0])

        if json_data["tipo_arquivo"] == "mineração":

            if "config_random" not in json_data or "itens" not in json_data["config_random"]:
                await interaction.followup.send("O JSON do comando não está no formato esperado para mineração.", ephemeral=True)
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

            await interaction.followup.send(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)



        elif json_data["tipo_arquivo"] == "universal":
        
            if "itens" not in json_data:
                await interaction.followup.send("O JSON do comando não está no formato esperado para o comando Universal.")
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
            await interaction.followup.send(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)
        

        elif json_data["tipo_arquivo"] == "loja":

            if "itens" not in json_data:
                await interaction.followup.send("O JSON do comando não está no formato esperado para loja.", ephemeral=True)
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
            await interaction.followup.send(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)

        elif json_data["tipo_arquivo"] == "procurado":

            if "itens" not in json_data:
                await interaction.followup.send("O JSON do comando não está no formato esperado para procurados.", ephemeral=True)
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
            await interaction.followup.send(f"Adicionadas {quantidade} categorias ao comando `{nome_cmd}`. Aqui está o arquivo atualizado para editar:", file=dc_file)






class customCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    bot.tree.add_command(JsonGroup())
    await bot.add_cog(customCommand(bot))