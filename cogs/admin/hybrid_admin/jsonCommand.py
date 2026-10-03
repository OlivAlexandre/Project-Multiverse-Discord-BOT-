import discord
from discord.ext import commands
from discord import app_commands
import json
import io
import os
import copy
from ui.jsonStyle import *
from utils import prefixo, whitelist_adm_prefix


class miningCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    



    @commands.hybrid_group(name="jsoncommand", description="Criação da parte de custom commands", invoke_without_command=True)
    async def custom_command_group(self, ctx: commands.Context):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.reply("Este comando não pode ser usado em mensagens diretas.")
            return

        await ctx.reply(f"Use um subcomando válido. Exemplo: `{prefixo_prefix}jsoncommand give` para baixar o JSON do comando customizado desejado.")
    

    
    @custom_command_group.command(name="give")
    @app_commands.autocomplete(tipo=autocomplete_jsons)
    @whitelist_adm_prefix()
    async def give_command(self, ctx: commands.Context, tipo: str, quantidade: int, nome_arquivo: str = None):
        prefixo_prefix = await prefixo(self.bot, ctx.message)

        if ctx.guild is None:
            await ctx.reply("Este comando não pode ser usado em mensagens diretas.")
            return

        os.makedirs("custom_commands", exist_ok=True)

        if tipo is None:
            await ctx.reply("Error: Coloque algum tipo!\n"
                           f"Os tipos existentes:\n{', '.join(jsons)}")
            return
        
        if quantidade is None:
            await ctx.reply("Error: Insira uma quantidade!")
            return

        if tipo not in jsons:
            await ctx.reply(f"Error: Tipo de comando inválido. Use `{', '.join(jsons)}`.")
            return

        
    
        if tipo == "mineração":

            dados_mining = copy.deepcopy(json_mining)
            dados_mining["config_random"]["itens"] = []

            for i in range(quantidade):
                dados_mining["config_random"]["itens"].append(
                    
                    {"nome": "Item", 
                     "raridade": "Comum/Incomum/Raro/Super Raro/Épico/Místico/Lendário", 
                     "chance": 999.999, 
                     "nivel_picareta": "nível", 
                     "curiosidade": "Curiosidade do item", 
                     "imagem": "https://link.com/item.png" },

                )
            
            with io.open("custom_commands/mining_command.json", "w", encoding="utf-8") as f:
                json.dump(dados_mining, f, ensure_ascii=False, indent=4)
            
            arquivo = discord.File("custom_commands/mining_command.json", filename="{}.json".format(nome_arquivo))
            await ctx.reply("Aqui está o modelo para o comando de mineração! Edite o arquivo JSON conforme necessário e depois envie para mim usando o comando `/admin customcommand upload <arquivo>`.", file=arquivo)

        elif tipo == "loja":

            dados_loja = copy.deepcopy(json_loja)
            dados_loja["itens"] = []

            for i in range(1, quantidade + 1):
                dados_loja["itens"].append(

                    {"id": f"{i} (pode trocar para o nome do próprio ou deixar número)",
                     "nome": "(Nome do item)",
                     "valor": 0,
                     "moeda": "yene/real/dolar",
                     "descricao": "(descrição do item)",
                     "tipo": "(tipo do item, se é uma arma, armadura, poção...)",
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
            
            with io.open("custom_commands/loja.json", "w", encoding="utf-8") as f:
                json.dump(dados_loja, f, ensure_ascii=False, indent=4)
            
            arquivo = discord.File  ("custom_commands/loja.json", filename="{}.json".format(nome_arquivo))
            await ctx.reply(f"Aqui está o modelo para comando de loja customizado! Edite o arquivo JSON conforme o necessário e depois envie para mim usando o comando `{prefixo_prefix}customcommand upload <arquivo>`.", file=arquivo)
        
        elif tipo == "procurado":

            dados_procurado = copy.deepcopy(json_procurado)
            dados_procurado["procurado"] = []

            for i in range(quantidade):
                dados_procurado["procurado"].append(

                    {"id": f"{i} (pode trocar para o nome do próprio ou deixar número)",
                     "nome": "(Nome do procurado)",
                     "raca": "(raça do procurado)",
                     "recompensa": "(recompensa ao conseguir)",
                     "descricao": "(descrição do procurado)",
                     "nivel_procurado": "F/E/D/C/B/A/S/SS",
                     "imagem": "link/imagem do procurado"},
                                  
                )
            
            with io.open("custom_commands/procurado.json", "w", encoding="utf-8") as f:
                json.dump(dados_procurado, f, ensure_ascii=False, indent=4)
            
            arquivo = discord.File("custom_commands/procurado.json", filename="{}.json".format(nome_arquivo))
            await ctx.reply(f"Aqui está o modelo para comando de lista de procurados! Edite o arquivo JSON conforme o necessário e depois envie para mim usando o comando `{prefixo_prefix}customcommand upload <arquivo>`.", file=arquivo)


        elif tipo == "clima":
        
            dados_clima = copy.deepcopy(json_clima)
            dados_clima["climas"] = []

            for i in range(quantidade):
                dados_clima["climas"].append(

                    {"emoji": "(algum emoji do clima escolhido)", 
                        "frase": "(alguma frase foda ae do clima)", 
                        "chance": 999.999, 
                        "temperatura": "Temperatura de 00ºC / Umidade de 00%... (você decide como estará)", 
                        "efeitos": "(efeito dos climas)",
                        "curiosidade": "(alguma curiosidade do clima ae)", 
                        "imagem": "https://link.com/item.png" },

                )

            with io.open("custom_commands/clima.json", "w", encoding="utf-8") as f:
                json.dump(dados_clima, f, ensure_ascii=False, indent=4)

            arquivo = discord.File("custom_commands/clima.json", filename="{}.json".format(nome_arquivo))
            await ctx.reply(f"Aqui está o modelo para comando de climas! Edite o arquivo JSON conforme o necessário e depois envie para mim usando o comando `/customcommand upload <arquivo>`.", file=arquivo)


        elif tipo == "universal":

            dados_all = copy.deepcopy(json_universal)
            dados_all["itens"] = []

            for i in range(quantidade):
                
                dados_all["itens"].append(

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

            with io.open("custom_commands/universal.json", "w", encoding="utf-8") as f:
                json.dump(dados_all, f, ensure_ascii=False, indent=4)

            arquivo = discord.File("custom_commands/universal.json", filename="{}.json".format(nome_arquivo))
            await ctx.reply(f"Aqui está o modelo para comando de lista de procurados! Edite o arquivo JSON conforme o necessário e depois envie para mim usando o comando `{prefixo_prefix}customcommand upload <arquivo>`.", file=arquivo)

        


    


    
    
    




async def setup(bot):
    await bot.add_cog(miningCommand(bot))