import discord
from discord.ext import commands
from discord import app_commands

jsons = ["mineração", "loja", "procurado", "clima", "universal"]
async def autocomplete_jsons(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    
    return [app_commands.Choice(name=tipo.capitalize(), value=tipo) 
            for tipo in jsons 
            if current.lower() in tipo.lower()
            ][:25]


json_mining = {

            "nome_comando": "(comando)",
            "tipo_comando": "random",
            "tipo_arquivo": "mineração",
            "texto_inicial": "Você está minerando nas minas de (----)!",
            "config_random": {
                "itens": [

                ]}
        }

json_procurado = {

            "nome_comando": "(comando de procurados de algum reino (ex.: procuradobritania))",
            "tipo_comando": "lista",
            "tipo_arquivo": "procurado",
            "texto_inicial": "Lista de procurados do reino (----)!",
                "procurado": [

                ]
        }

json_loja = {

            "nome_comando": "(comando da loja (ex.: lojacaverna))",
            "tipo_comando": "lista",
            "tipo_arquivo": "loja",
            "texto_inicial": "Loja de (----)!",
                "itens": [

                ]
        }


json_clima = {

            "nome_comando": "(comando do clima (ex.: clima-dia))",
            "tipo_comando": "random",
            "tipo_arquivo": "clima",
            "texto_inicial": "BOM DIA!!!",
            "hora_inicial": "dia, noite...",
            "emoji_hora": "emoji do horário (ex.: ☀️, 🌙...)",
                "climas": [

                ]
        }


json_universal = {
                
                "nome_comando": "",
                "tipo_comando": "random",
                "tipo_arquivo": "(ex.: mineração, daily, loja, procurado, clima)",
                "type": "all",
                "inicial": {
                        "type": "(ex.: 'Resultado da roleta')",
                        "line": "(linha do seu type) - ex.: 'Você roletou e ganhou...'",
                        "emoji": "(emoji do seu type)"
                },
                "starter": {
                        "type": "(ex.: 'Tipo inicial')",
                        "line": "(linha do seu type) - ex.: 'Tipo dia...'",
                        "emoji": "(emoji do seu type)"
                },
                "itens": [
                    
                ],
                
}