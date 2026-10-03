import re

import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import json
import random
from utils import prefixo, busca_molde




async def process_command(bot: commands.Bot, mensagem: discord.Message, canal: discord.TextChannel, guild_id: int, author: discord.User, nome_comando: str, ping: discord.Role):
    prefixos = await prefixo(bot, mensagem)
    
    conn = sqlite3.connect('json.db')
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute('''SELECT command_name, type_command, type_archive, type, json_data, template_text 
                        FROM custom_command 
                        WHERE guild_id = ? AND command_name = ?''', 
                        (int(guild_id), nome_comando))
    resultado = cursor.fetchone()

    print(f"[DEBUG] Resultado encontrado no banco: {resultado}")
    conn.close()

    if not resultado:
        return False
    
    nome_comando, tipo_comando, tipo_arquivo, type, json_data, template_text = resultado
    print(f"[CHECKING] Olhando arquivos...\n\n- Tipo arquivo: {tipo_arquivo}\n\n- Type... {type}")
    dados_comandos = json.loads(json_data)
    tipo_arquivo = dados_comandos.get("tipo_arquivo", "comum").lower().strip()

    if resultado:
            

            if tipo_comando == "random":
                
                if tipo_arquivo == 'mineração':
                    lista_itens = dados_comandos["config_random"]["itens"]
                    

                    item_sorteado = random.choices(
                        lista_itens, 
                        weights=[float(item["chance"]) for item in lista_itens],
                        k=1
                    )[0]

                    conn = sqlite3.connect('json.db')
                    cursor = conn.cursor()

                    cursor.execute('''SELECT template_text FROM templates WHERE guild_id = ? AND type_archive = ?''',
                                (int(guild_id), tipo_arquivo))
                    resultado_template = cursor.fetchone()
                    template_grupo = resultado_template[0] if resultado_template else None

                    conn.close()

                    molde_final = None

                    if template_text:
                        molde_final = template_text
                    elif template_grupo:
                        molde_final = template_grupo

                    if molde_final:
                        url_imagem = item_sorteado.get("imagem", "")
                        resposta_final = (
                            molde_final.replace("[item]", item_sorteado["nome"])
                                    .replace("[nome do item]", item_sorteado["nome"])

                                    .replace("[user]", author.mention)
                                    .replace("[usuário]", author.mention)
                                    .replace("[User]", author.mention)
                                    .replace("[Usuário]", author.mention)
                                    .replace("[menção]", author.mention)
                                    .replace("[pessoa]", author.mention)

                                    .replace("[nivel de picareta]", item_sorteado["nivel_picareta"])
                                    .replace("[nivel da picareta]", item_sorteado["nivel_picareta"])
                                    .replace("[nivel picareta]", item_sorteado["nivel_picareta"])

                                    .replace("[chance]", str(item_sorteado["chance"]))
                                    .replace("[porcentagem]", str(item_sorteado["chance"]))
                                    .replace("[raridade]", str(item_sorteado["chance"]))
                        )

                        if url_imagem:
                            resposta_final = resposta_final.replace("[imagem do item]", url_imagem)
                            resposta_final = resposta_final.replace("[link]", url_imagem)
                            resposta_final = resposta_final.replace("[imagem]", url_imagem)
                        
                        else:
                            resposta_final = resposta_final.replace("[imagem]", "")
                            resposta_final = resposta_final.replace("[imagem do item]", "")
                            resposta_final = resposta_final.replace("[link]", "")
                        
                        await canal.send(resposta_final)
                        return
                    
                    else:
                        cores_raridade = {
                            "Comum": discord.Color.light_gray(),
                            "Incomum": discord.Color.dark_gray(),
                            "Raro": discord.Color.dark_orange(),
                            "Super raro": discord.Color.teal(),
                            "Épico": discord.Color.purple(),
                            "Místico": discord.Color.red(),
                            "Lendário": discord.Color.gold()
                        }
                        cor_final = cores_raridade.get(item_sorteado["raridade"], discord.Color.dark_theme())

                        embed = discord.Embed(
                            title=f"⛏️ Resultado da mineração!",
                            description=f"{author.mention} {dados_comandos['texto_inicial']}\n\nVocê obteve: **{item_sorteado['nome']}**!",
                            color=cor_final
                        )

                        embed.add_field(name="💎 Raridade", value=item_sorteado["raridade"], inline=False)

                        if item_sorteado["nivel_picareta"]:
                            embed.add_field(name="⛏ Nível da Picareta", value=item_sorteado["nivel_picareta"], inline=False)
                        
                        if item_sorteado["curiosidade"]:
                            embed.add_field(name="📚 Curiosidade", value=f"*- {item_sorteado['curiosidade']}*", inline=False)
                        
                        embed.set_footer(text="Rode o dado para saber a quantidade conseguida e aguarde 3 minutos para usar o comando novamente.")
                        if item_sorteado["imagem"]:
                            embed.set_image(url=item_sorteado["imagem"])
                        
                        await canal.send(embed=embed)
                        return
                


                elif tipo_arquivo == "clima":

                    climas = dados_comandos["climas"]

                    clima_sorteado = random.choices(
                        climas, 
                        weights=[float(clima["chance"]) for clima in climas],
                        k=1
                    )[0]

                    emoji = clima_sorteado.get("emoji", "")
                    frase = clima_sorteado.get("frase", "")
                    efeitos = clima_sorteado.get("efeitos", "")
                    curiosidade = clima_sorteado.get("curiosidade", "")
                    temperatura = clima_sorteado.get("temperatura", "")

                    texto_inicial = dados_comandos.get("texto_inicial", "")
                    hora_inicial = dados_comandos.get("hora_inicial", "")
                    emoji_hora = dados_comandos.get("emoji_hora", "")

                    if hora_inicial.lower() == "dia":
                        clim = "do Dia"
                    
                    elif hora_inicial.lower() == "noite":
                        clim = "da Noite"

                    elif hora_inicial.lower() == "tarde":
                        clim = "da Tarde"
                    else:
                        clim = "do Clima"
                    
                    ping_role = ping.mention

                    conn = sqlite3.connect('json.db')
                    cursor = conn.cursor()
                    cursor.execute('''SELECT template_text FROM templates WHERE guild_id = ? AND type_archive = ?''',
                                (int(guild_id), tipo_arquivo))
                    resultado_template = cursor.fetchone()
                    template_grupo = resultado_template[0] if resultado_template else None

                    conn.close()

                    molde_final = None

                    if template_text:
                        molde_final = template_text
                    elif template_grupo:
                        molde_final = template_grupo

                    if molde_final:
                        url_imagem = clima_sorteado.get("imagem", "")
                        resposta_final = (
                            molde_final.replace("[emoji]", emoji)
                                    .replace("[emoji da hora]", emoji_hora)
                                    .replace("[emoji do dia]", emoji_hora)
                                    .replace("[emoji do clima]", emoji_hora)

                                    .replace("[frase]", frase)
                                    .replace("[fala]", frase)

                                    .replace("[dia]", hora_inicial)
                                    .replace("[noite]", hora_inicial)

                                    .replace("[dia/noite]", clim)
                                    .replace("[do dia/noite]", clim)
                                    .replace("[do clima]", clim)

                                    .replace("[menção]", ping_role)
                                    .replace("[ping]", ping_role)
                                    .replace("[cargo]", ping_role)

                                    .replace("[efeito]", efeitos)
                                    .replace("[ganhos]", efeitos)

                                    .replace("[curiosidade]", curiosidade)

                                    .replace("[temperatura]", temperatura)
                                    .replace("[temp]", temperatura)
                                    .replace("[temp.]", temperatura)
                        )
                        if url_imagem:
                            resposta_final = resposta_final.replace("[gif]", url_imagem)
                            resposta_final = resposta_final.replace("[link]", url_imagem)
                            resposta_final = resposta_final.replace("[imagem]", url_imagem)
                            resposta_final = resposta_final.replace("[img]", url_imagem)
                            resposta_final = resposta_final.replace("[image]", url_imagem)

                        else:
                            resposta_final = resposta_final.replace("[gif]", "")
                            resposta_final = resposta_final.replace("[link]", "")
                            resposta_final = resposta_final.replace("[imagem]", "")
                            resposta_final = resposta_final.replace("[img]", "")
                            resposta_final = resposta_final.replace("[image]", "")

                        await canal.send(resposta_final)
                        return
                    
                    else:
                        embed = discord.Embed(
                            title=f"{emoji} -- Clima {clim} ({emoji_hora})!",
                            description=f"{texto_inicial}",
                            color=discord.Color.blue()
                        )

                        embed.add_field(name=f"{emoji} Clima", value="", inline=False)
                        if frase:
                            embed.add_field(name="", value=f"{frase}", inline=False)
                        if temperatura:
                            embed.add_field(name=f"Temperatura {clim}: ", value=f"{temperatura}", inline=True)
                        if efeitos:
                            embed.add_field(name="Efeitos do clima: ", value=f"{efeitos}", inline=False)
                        if curiosidade:
                            embed.add_field(name="Curiosidades", value=f"{curiosidade}", inline=False)

                        if clima_sorteado.get("imagem"):
                            embed.set_image(url=clima_sorteado["imagem"])
                        
                        await canal.send(content=ping_role, embed=embed)
                        return

                if type == "all":
                    print(f"[CHECKING] Encontrado, arquivo com type '{type}'")
                    itens = dados_comandos["itens"]

                    if not itens:
                        return await canal.send("nenhum item configurado para este comando...")

                    item_sorteado = random.choices(
                        itens, 
                        weights=[float(item["chance"]) for item in itens],
                        k=1
                    )[0]
                    
                    bloco_inicial = dados_comandos.get("inicial", {})
                    type_inicial = bloco_inicial.get("type", "").strip()
                    line_inicial = bloco_inicial.get("line", "").strip()
                    emoji_inicial = bloco_inicial.get("emoji", "").strip()


                    bloco_starter = dados_comandos.get("starter", {})
                    type_starter = bloco_starter.get("type", "").strip()
                    line_starter = bloco_starter.get("line", "").strip()
                    emoji_starter = bloco_starter.get("emoji", "").strip()


                    if "type" in bloco_inicial and not type_inicial:
                        print("[WARNING] - O bloco 'inicial' possui seu tipo, mas está vazio.")

                    nome_item = item_sorteado.get("name", "")
                    emoji_item = item_sorteado.get("emoji_item", "")
                    sufixo_item = item_sorteado.get("sufixo", "")
                    chance = item_sorteado["chance"]
                    url_imagem = item_sorteado.get("imagem", "")

                    completo = f"{emoji_item} {nome_item} {sufixo_item}".strip()


                    title_inicial = f"{emoji_inicial} {type_inicial}".strip() if type_inicial else "Resultado"
                    linha_inicial = f"{author.mention} {line_inicial}" if line_inicial else f"{author.mention} usou o comando."


                    subs = {
                        "user": author.mention,
                        "ping": author.mention,
                        "usuário": author.mention,
                        "usuario": author.mention,
                        "menção": author.mention,
                        "mencao": author.mention,
                        "pessoa": author.mention,

                        "item": nome_item,
                        "name": nome_item,
                        "nome": nome_item,
                        "nome do item": nome_item,

                        "sufixo": sufixo_item,
                        "sufixo_item": sufixo_item,
                        "sufixo do item": sufixo_item,

                        "emoji_item": emoji_item,
                        "emoji item": emoji_item,
                        "emoji do item": emoji_item,
                        "emoji": emoji_item,

                        "chance": str(chance),
                        "porcentagem": str(chance),
                        "raridade": str(chance),

                        "imagem": url_imagem,
                        "url": url_imagem,
                        "link": url_imagem,

                        "inicial": line_inicial,
                        "starter": line_starter,
                    }

                    def formatar_T(texto):
                        if not texto:
                            return ""

                        def substituir_tag(match):
                            tag = match.group(1).strip().lower()

                            if tag.isdigit():
                                return f"<@&{tag}>"

                            for chave_mapa, valor_mapa in subs.items():
                                if chave_mapa.lower() == tag:
                                    return valor_mapa
                            return match.group(0)
                        
                        return re.sub(r"\[(.*?)\]", substituir_tag, texto, flags=re.IGNORECASE)
                

                    if line_inicial:
                        linha_inicial = formatar_T(line_inicial)
                    else:
                        linha_inicial = f"{author.mention} usou o comando."


                    campos_embed = []


                    for chave, bloco in item_sorteado.items():
                        if chave.startswith("text") and isinstance(bloco, dict):
                            type_text = bloco.get("type", "").strip()
                            emoji_text = bloco.get("emoji", "").strip()

                            if "type" in bloco and not type_text:
                                print(f"[WARNING] - Chave type {chave} está presente, mas vazio.")
                            

                            l1 = bloco.get("line1", "")
                            l2 = bloco.get("line2", "")
                            l3 = bloco.get("line3", "")
                            l4 = bloco.get("line4", "")
                            l5 = bloco.get("line5", "")
                            l6 = bloco.get("line6", "")
                            l7 = bloco.get("line7", "")
                            l8 = bloco.get("line8", "")
                            l9 = bloco.get("line9", "")
                            l10 = bloco.get("line10", "")
                            l11 = bloco.get("line11", "")
                            l12 = bloco.get("line12", "")
                            l13 = bloco.get("line13", "")

                            linhas_brutas = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13]
                            linhas_validas = [l if l == '\n' else formatar_T(l)
                                                 for l in linhas_brutas if l == "\n" or l.strip()]
                            conteudo_campo = "\n".join(linhas_validas)

                            if type_text:
                                print("[CHECKING] Seu type text... checando...")
                                title_parte = f"{emoji_text} {type_text}".strip()

                                if conteudo_campo:
                                    campos_embed.append((title_parte, conteudo_campo))
                                
                                subs[type_text] = conteudo_campo
                                subs[f"{type_text}_emoji"] = emoji_text
                                subs["ping"] = author.mention
                                subs["user"] = author.mention

                    
                    
                    molde_final = busca_molde(
                        guild_id=int(guild_id),
                        nome_comando=nome_comando,
                        tipo_arquivo=tipo_arquivo,
                        template=template_text
                    )

                    if molde_final:
                        resposta_final = formatar_T(molde_final)

                        if url_imagem:
                            resposta_final = resposta_final.replace("[imagem do item]", url_imagem)
                            resposta_final = resposta_final.replace("[link]", url_imagem)
                            resposta_final = resposta_final.replace("[imagem]", url_imagem)
                        
                        else:
                            resposta_final = resposta_final.replace("[imagem]", "")
                            resposta_final = resposta_final.replace("[imagem do item]", "")
                            resposta_final = resposta_final.replace("[link]", "")
                        
                        await canal.send(resposta_final)
                        return
                    
                    else:
                        print("[CHECKING] Preparando o embed . . .")

                        embed = discord.Embed(
                            title=title_inicial,
                            description=linha_inicial,
                            color=discord.Color.gold()
                        )

                        embed.add_field(name=f"___***{completo}***___", value="\n\n", inline=False)

                        for titulo, conteudo in campos_embed:
                            embed.add_field(name=titulo, value=conteudo, inline=False)

                        if url_imagem:
                            embed.set_image(url=url_imagem)

                        await canal.send(embed=embed)
                        return









            








            elif tipo_comando == 'lista':

                no_prefix = mensagem.content[len(prefixos):].strip()
            
                if not no_prefix:
                    return


                parte = no_prefix.split()
                if not parte:
                    return

                argumentos = parte[1:]

                if tipo_arquivo == "loja":

                    lista_itens = dados_comandos.get("itens", [])

                    if not argumentos:
                        
                        texto_loja = dados_comandos.get("texto_inicial", "Loja!")
                        embed = discord.Embed(
                            title=texto_loja,
                            description=f"Use {prefixos}{nome_comando} view <item> para visualizar melhor o item",
                            color=discord.Color.gold()
                        )
                        for item in lista_itens:
                            embed.add_field(
                                name=f"{item.get('nome', 'Item')}",
                                value=f"ID: `{item.get('id')}` | Preço: 💰 {item.get('valor', item.get('preco', 0))}",
                                inline=False
                            )
                        await canal.send(embed=embed)
                        return
                    

                    primeiro_argumento = argumentos[0].strip().lower()
                    sub_item = None

                    if primeiro_argumento in ['buy', 'comprar', 'obter']:
                        acao = 'buy'
                        if len(argumentos) > 1:
                            sub_item = argumentos[1].lower().strip()
                        
                        elif primeiro_argumento in ['view', 'ver', 'checar', 'olhar']:
                            acao = 'view'
                            if len(argumentos) > 1:
                                sub_item = argumentos[1].lower().strip()
                        
                        else:
                            acao = 'view'
                            sub_item = primeiro_argumento
                        
                        if not sub_item:
                            await canal.send(f"Especifique o item! Exemplo: {prefixos}{nome_comando} {acao} 1")
                        
                        item_info = None
                        for item in lista_itens:
                            if str(item.get("id", "")).lower().strip() == sub_item:
                                item_info = item
                                break
                        
                        if not item_info:
                            await canal.send(f"O item `{argumentos[1] if len(argumentos)>1 else argumentos[0]}` não foi encontrado!")
                            return


                        if acao == "view":
                            titulo_embed = item_info.get("nome", f"Item {sub_item}")
                            descricao_embed = item_info.get("descrição", item_info.get("descricao", "Sem descrição disponível."))

                            embed = discord.Embed(
                                title=titulo_embed,
                                description=descricao_embed,
                                color=discord.Color.dark_gold()
                            )

                            if "nome" in item_info:
                                embed.add_field(name="📝 Nome", value=f"{item_info['nome']}", inline=False)

                            if "dano" in item_info:
                                embed.add_field(name="⚔ Dano", value=f"{item_info['dano']}", inline=False)
                            
                            if "gasto" in item_info:
                                embed.add_field(name="🌀 Custo", value=f"{item_info['gasto']}", inline=False)

                            if "raca" in item_info:
                                embed.add_field(name="🧑 Raça", value=f"{item_info['raca']}", inline=False)

                            if "tipo" in item_info:
                                embed.add_field(name="⚔ Tipo", value=f"{item_info['tipo']}", inline=False)

                            if "valor" in item_info:
                                embed.add_field(name="💰 Valor", value=f"{item_info['valor']}", inline=False)
                            
                            if "itens" in item_info:
                                itens_list = item_info["itens"]
                                itens_texto = "\n".join([f"- {item}" for item in itens_list])
                                embed.add_field(name="📦 Itens", value=itens_texto, inline=False)

                                if "status" in item_info and isinstance(item_info["status"], dict):
                                    status_info = item_info["status"]
                                    textos_atribuidos = ""

                                    if "forca" in status_info and str(status_info["forca"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                        textos_atribuidos += f"***Força:*** `{status_info['forca']}`\n"
                                    
                                    if "hp" in status_info and str(status_info["hp"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                        textos_atribuidos += f"***HP:*** `{status_info['hp']}`\n"
                                    
                                    if "energia" in status_info and str(status_info["energia"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                        textos_atribuidos += f"***Energia:*** `{status_info['energia']}`\n"
                                    
                                    if "vigor" in status_info and str(status_info["vigor"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                        textos_atribuidos += f"***Vigor:*** `{status_info['vigor']}`\n"
                                    
                                    if "velocidade" in status_info and str(status_info["velocidade"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                        textos_atribuidos += f"***Velocidade:*** `{status_info['velocidade']}`\n"
                                    
                                    if textos_atribuidos:
                                        embed.add_field(name="# Status/Atributos:",
                                                        value=textos_atribuidos, inline=False)
                            
                            if "efeitos" in item_info:
                                embed.add_field(name="🧪 Efeitos", value=f"{item_info['efeitos']}", inline=False)
                            
                            if "tipo" in item_info:
                                embed.add_field(name="⁉ Tipo", value=f"{item_info['tipo']}", inline=False)
                            
                            if "rank" in item_info:
                                embed.add_field(name="🔰 Rank", value=f"{item_info['rank']}", inline=False)
                            
                            if "nivel_procurado" in item_info:
                                embed.add_field(name="🏴‍☠️ Nível de procurado", value=f"{item_info['nivel_procurado']}", inline=False)
                            
                            if "descricao" in item_info:
                                embed.add_field(name="🧾 Descrição", value=f"{item_info['descricao']}", inline=False)
                            
                            if "elemento" in item_info:
                                embed.add_field(name="🔥 Elemento", value=f"{item_info['elemento']}", inline=False)

                            if "recompensa" in item_info:
                                embed.add_field(name="💰 Recompensa", value=f"{item_info['recompensa']}", inline=False)
                            
                            if "curiosidade" in item_info:
                                embed.add_field(name="💭 Curiosidade", value=f"{item_info['curiosidade']}", inline=False)
                            
                            
                            url_imagem = item_info.get("imagem", "")
                            if url_imagem and str(url_imagem).startswith("http"):
                                embed.set_image(url=url_imagem)

                            elif mensagem.guild and mensagem.guild.icon:
                                embed.set_image(url=mensagem.guild.icon.url)

                            
                            embed.set_footer(text=f"Consulta: {prefixos}{nome_comando} {argumentos[0]}")
                            await canal.send(embed=embed)
                        
                        elif acao == "buy":
                            await canal.send(f"{mensagem.author.mention} comprou **{item_info.get('nome')}**!!")
                            return


                        else:
                            await canal.send(f"Ops! O item `{argumentos[0]}` não existe nesse comando...")
                        return
                
                else:

                    todos_itens = []
                    for chave, valor in dados_comandos.items():
                        if chave == "tipo_arquivo":
                            continue
                        if isinstance(valor, list):
                            todos_itens.extend(valor)
                        elif isinstance(valor, dict):
                            todos_itens.append(valor)


                    if not argumentos:
                        embed = discord.Embed(
                            title=f"Lista dos procurados de `{nome_comando}`",
                            description=f"Use {prefixos}{nome_comando} <ID> para visualizar melhor o item",
                            color=discord.Color.dark_gold()
                        )
                        for item in todos_itens:
                            if isinstance(item, dict):
                                item_id = str(item.get("id", "")).lower().strip()
                                item_nome = item.get("nome", "Item")
                                procurado = item.get("nivel_procurado", "Nível desconhecido")
                                embed.add_field(name=f"ID: {item_id}", value=f"Nome: **{item_nome}**\nNível de procurado: {procurado}", inline=False)

                        await canal.send(embed=embed)
                        return
                    
                    if argumentos[0].lower().strip() in ['view', 'ver', 'checar', 'olhar']:
                        if len(argumentos) > 1:
                            sub_item = argumentos[1].lower().strip()
                        
                        else:
                            await canal.send(f"Ops! Você usou {argumentos[0]}, mas não informou o que deseja consultar.")
                            return
                    
                    else:
                        sub_item = argumentos[0].lower().strip()
                    

                    item_info = None
                    for item in todos_itens:
                        if isinstance(item, dict):
                            item_id = str(item.get("id", "")).lower().strip()
                            if item_id == sub_item:
                                item_info = item
                                break

                    if item_info:
                        titulo_embed = item_info.get("nome", f"Item {sub_item}")
                        descricao_embed = item_info.get("descrição", item_info.get("descricao", "Sem descrição disponível."))

                        embed = discord.Embed(
                            title="Você está vendo um dos procurados",
                            description="--- Cartaz de procurado ---",
                            color=discord.Color.dark_gold()
                        )

                        if "nome" in item_info:
                            embed.add_field(name="📝 Nome", value=f"{item_info['nome']}", inline=False)

                        if "raca" in item_info:
                            embed.add_field(name="🧑 Raça", value=f"{item_info['raca']}", inline=False)

                        if "dano" in item_info:
                            embed.add_field(name="⚔ Dano", value=f"{item_info['dano']}", inline=False)
                        
                        if "gasto" in item_info:
                            embed.add_field(name="🌀 Custo", value=f"{item_info['gasto']}", inline=False)
                        
                        if "valor" in item_info:
                            embed.add_field(name="💰 Valor", value=f"{item_info['valor']}", inline=False)
                        
                        if "recompensa" in item_info:
                            embed.add_field(name="💰 Recompensa", value=f"{item_info['recompensa']}", inline=False)

                        if "itens" in item_info:
                            itens_list = item_info["itens"]
                            itens_texto = "\n".join([f"- {item}" for item in itens_list])
                            embed.add_field(name="📦 Itens", value=itens_texto, inline=False)

                            if "status" in item_info and isinstance(item_info["status"], dict):
                                status_info = item_info["status"]
                                textos_atribuidos = ""

                                if "forca" in status_info and str(status_info["forca"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                    textos_atribuidos += f"***Força:*** `{status_info['forca']}`\n"
                                
                                if "hp" in status_info and str(status_info["hp"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                    textos_atribuidos += f"***HP:*** `{status_info['hp']}`\n"
                                
                                if "energia" in status_info and str(status_info["energia"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                    textos_atribuidos += f"***Energia:*** `{status_info['energia']}`\n"
                                
                                if "vigor" in status_info and str(status_info["vigor"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                    textos_atribuidos += f"***Vigor:*** `{status_info['vigor']}`\n"
                                
                                if "velocidade" in status_info and str(status_info["velocidade"]).strip().lower() not in ["0", "x0", "", 0, "Nenhum", "nenhum"]:
                                    textos_atribuidos += f"***Velocidade:*** `{status_info['velocidade']}`\n"
                                
                                if textos_atribuidos:
                                    embed.add_field(name="# Status/Atributos:",
                                                    value=textos_atribuidos, inline=False)
                        
                        if "efeitos" in item_info:
                            embed.add_field(name="🧪 Efeitos", value=f"{item_info['efeitos']}", inline=False)
                        
                        if "tipo" in item_info:
                            embed.add_field(name="⁉ Tipo", value=f"{item_info['tipo']}", inline=False)
                        
                        if "rank" in item_info:
                            embed.add_field(name="🔰 Rank", value=f"{item_info['rank']}", inline=False)
                        
                        if "nivel_procurado" in item_info:
                            embed.add_field(name="🏴‍☠️ Nível de procurado", value=f"{item_info['nivel_procurado']}", inline=False)
                        
                        if "descricao" in item_info:
                            embed.add_field(name="🧾 Descrição", value=f"{item_info['descricao']}", inline=False)
                        
                        if "elemento" in item_info:
                            embed.add_field(name="🔥 Elemento", value=f"{item_info['elemento']}", inline=False)
                        
                        if "curiosidade" in item_info:
                            embed.add_field(name="💭 Curiosidade", value=f"{item_info['curiosidade']}", inline=False)
                        
                        
                        url_imagem = item_info.get("imagem", "")
                        if url_imagem and str(url_imagem).startswith("http"):
                            embed.set_image(url=url_imagem)
                        elif mensagem.guild and mensagem.guild.icon:
                            embed.set_image(url=mensagem.guild.icon.url)
                        
                        embed.set_footer(text=f"Consulta: {prefixos}{nome_comando} {argumentos[0]}")
                        await canal.send(embed=embed)
                    else:
                        await canal.send(f"Ops, nenhum item com ID `{sub_item}` foi encontrado.")
                    
            return




class motorCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance (error, commands.CommandNotFound):
            return
        
        raise error
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or not message.guild:
            return
        
        if not message.guild:
            await self.process_commands(message)
            return

        prefixos = await prefixo(self.bot, message)

        if not message.content.startswith(prefixos):
            return
        
        no_prefix = message.content[len(prefixos):].strip()

        if not no_prefix:
            return
    
        parte = no_prefix.split()
        if not parte:
            return
        
        role = None

        if len(parte) > 1:
            possivel_role = parte[1].strip()
            id_limpo = re.sub(r'\D', '', possivel_role)

            if id_limpo.isdigit():
                role_id = int(id_limpo)
                role = message.guild.get_role(role_id)

        nome_comando = parte[0].lower().strip()

        nativo = self.bot.get_command(nome_comando)

        if nativo is not None:
            return

        await process_command(bot=self.bot, mensagem=message, canal=message.channel, guild_id = message.guild.id, author = message.author, nome_comando=nome_comando, ping=role)
        

        
        

        
    
async def setup(bot):
    await bot.add_cog(motorCommands(bot))