import discord
from discord.ext import commands
from discord import app_commands
from utils import Paginador, whitelist_adm_prefix, prefixo


class NormalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    














    @commands.hybrid_command(name="helpall")
    @whitelist_adm_prefix()
    async def helpStaff(self, ctx: commands.Context):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        embed = discord.Embed(
            title="Ajuda Completa para Staff - Página 1",
            description="Aqui estão todos os comandos de ajuda disponíveis para a equipe de administração, alguns comandos são mistos para slash e prefixos, siga a página.",
            color=discord.Color.purple()
        )

        embed.add_field(name="Lista das páginas", value="Nesta página, veja onde estão cada comando em qual página.\n\n\n1. Lista\n2. Prefixos\n3. Comandos Customizáveis\n4. Moldes\n5. Whitelist\n6. Comandos de tutoriais\n7. Comuns (Ainda admin)\n8. Arquivos dos comandos customizáveis", inline=False)

        embed1 = discord.Embed(
            title="Comandos para os prefixos (Misto) - Página 2",
            description=f"Todos os comandos para mudar os prefixos (atual prefixo: `{prefixo_prefix}`).",
            color=discord.Color.purple()
        )
        
        embed1.add_field(name=f"{prefixo_prefix}prefix set <prefix>", value="Adiciona um novo prefixo para o servidor.", inline=False)
        embed1.add_field(name=f"{prefixo_prefix}prefix reset <prefix>", value="Reseta o prefixo existente do servidor para o padrão.", inline=False)
        embed1.add_field(name=f"{prefixo_prefix}prefix view", value="Vê o prefixo configurado do servidor.", inline=False)


        embed2 = discord.Embed(
            title="Comandos para os comandos customizáveis/criáveis (Misto) - Página 3",
            description="Todos os comandos para criar, deletar, baixar e listar os comandos customizáveis do servidor.",
            color=discord.Color.purple()
        )

        embed2.add_field(name=f"{prefixo_prefix}customcommand add <nome> <quantidade>", value="Adiciona mais slots a um comando customizado existente.", inline=False)
        embed2.add_field(name=f"{prefixo_prefix}customcommand upload <nome> <arquivo>", value="Adiciona um novo custom command para o servidor.", inline=False)
        embed2.add_field(name=f"{prefixo_prefix}customcommand delete <nome>", value="Remove um custom command existente do servidor.", inline=False)
        embed2.add_field(name=f"{prefixo_prefix}customcommand list", value="Lista todos os custom commands configurados para o servidor.", inline=False)
        embed2.add_field(name=f"{prefixo_prefix}customcommand download <nome>", value="Baixa o arquivo JSON de um custom command específico do servidor.", inline=False)

        embed3 = discord.Embed(
            title="Comandos para moldes dos comandos customizáveis (Misto) - Página 4",
            description="Todos os comandos para manipular os moldes dos comandos customizáveis do servidor.",
            color=discord.Color.purple()
        )

        embed3.add_field(name=f"{prefixo_prefix}molde help", value="Checa o help dos moldes e o que fazer para modificar.", inline=False)
        embed3.add_field(name=f"{prefixo_prefix}molde set <tipo> <molde (RECOMENDADO EM PREFIXO)>", value="Adiciona o molde ou a um tipo (mineração, daily...), ou em um comando específico.", inline=False)
        embed3.add_field(name=f"{prefixo_prefix}molde view <tipo>", value="Vê o molde usado de um tipo, ou em um comando específico.", inline=False)
        embed3.add_field(name=f"{prefixo_prefix}molde delete <tipo>", value="Deleta o molde usado de um tipo de comando, ou do comando em específico.", inline=False)

        embed4 = discord.Embed(
            title="Comandos para a whitelist (Slash (/)) - Página 5",
            description="Todos os comandos para adicionar ou remover usuários da whitelist.",
                color=discord.Color.purple()
            )

        embed4.add_field(name=f"/whitelist add <menção>", value="Adiciona um cargo ou usuário a uma whitelist de quem pode usar comandos de administração.", inline=False)
        embed4.add_field(name=f"/whitelist remove <menção>", value="Remove um cargo ou usuário a uma whitelist.", inline=False)
        embed4.add_field(name=f"/whitelist list", value="Lista de usuários na whitelist.", inline=False)

        embed5 = discord.Embed(
            title="Comandos de tutoriais (Misto) - Página 6",
            description="Todos os comandos de tutorial para administradores.",
            color=discord.Color.purple()
        )

        embed5.add_field(name=f"{prefixo_prefix}tutorial", value="Checa o tutorial básico do bot sobre como usar a parte de custom command.", inline=False)
        #embed5.add_field(name="Por hora só possui esse, mas breve pode haver mais!", value="", inline=False)

        embed6 = discord.Embed(
            title="Comandos comuns (Ainda admin) / (Misto) - Página 7",
            description="Todos os comandos padrões.",
            color=discord.Color.purple()
        )

        embed6.add_field(name=f"{prefixo_prefix}ping", value="Checa a latência do bot.", inline=False)
        embed6.add_field(name=f"{prefixo_prefix}backup [install/insert] <arquivo>", value="Faz backup do banco de dados do bot, ou insere um novo backup.", inline=False)
        embed6.add_field(name=f"{prefixo_prefix}helpall", value="Mostra todos os comandos de prefixo e custom command para administradores (esse mesmo que você vê).", inline=False)

        embed7 = discord.Embed(
            title="Comandos dos arquivos dos comandos customizáveis (Misto) - Página 8",
            description="Todos os comandos para pegar os arquivos JSON dos comandos customizáveis do servidor.",
            color=discord.Color.purple()
        )

        embed7.add_field(name=f"{prefixo_prefix}jsoncommand give <tipo> <quantidade>", value="Gera um arquivo JSON de modelo para o tipo de comando customizável desejado (os padrões existentes: mineração, daily, loja ou procurado).", inline=False)


        embed8 = discord.Embed(
            title="Comandos de alteração do bot (''Misto'') - Página 9",
            description="Todos os comandos para modificar tanto a foto, banner e/ou até status do bot",
            color=discord.Color.purple()
        )
        embed8.add_field(name=f"{prefixo_prefix}avatar [set/view]", value="Altera ou vê o avatar do bot.", inline=False)
        embed8.add_field(name=f"{prefixo_prefix}banner [set/view]", value="Altera ou vê o banner do bot.", inline=False)

        embed8.add_field(name=f"/status change <mudança> <texto> <link (apenas para streaming)>", value="Altera ou vê o status do bot.", inline=False)


        embedall = [embed, embed1, embed2, embed3, embed4, embed5, embed6, embed7, embed8]
        view = Paginador(paginas=embedall)
        await ctx.send(embed=embedall[0], view=view)














    @commands.hybrid_group(name="backup", description="[STAFF] Comando para backup do banco de dados do bot", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def backup_command(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.reply("Este comando não pode ser usado em mensagens diretas.")
            return

        await ctx.reply("Por favor, use o comando `/backup install` para baixar o backup ou `/backup insert <arquivo>` para inserir um novo backup.")






    @backup_command.command(name="install", description="[STAFF] Baixa o backup do banco de dados do bot")
    @commands.has_permissions(administrator=True)
    async def backup_install(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.reply("Este comando não pode ser usado em mensagens diretas.")
            return

        try:
            arquivo = discord.File("json.db", filename="json.db")
            await ctx.reply("Aqui está o backup do banco de dados do bot:", file=arquivo)
        except Exception as e:
            await ctx.reply(f"Ocorreu um erro ao tentar enviar o backup: {e}")














    
    @backup_command.command(name="insert", description="[STAFF] Insere um novo backup no banco de dados do bot")
    @app_commands.describe(file="O arquivo de backup a ser inserido (deve ser um arquivo ''.db'' válido).")
    @commands.has_permissions(administrator=True)
    async def backup_insert(self, ctx: commands.Context, file: discord.Attachment = None):
        if ctx.guild is None:
            await ctx.reply("Este comando não pode ser usado em mensagens diretas.")
            return

        if file is None:
            await ctx.reply("Por favor, envie um arquivo para inserir no banco de dados.")
            return

        if not file.filename.endswith(".db"):
            await ctx.reply("O arquivo enviado não é um arquivo de banco de dados válido (.db).")
            return

        try:
            await file.save("json.db")
            await ctx.reply("O banco de dados foi atualizado com sucesso!")
        except Exception as e:
            await ctx.reply(f"Ocorreu um erro ao tentar atualizar o banco de dados: {e}")
            

    












    @commands.hybrid_command(name="tutorial", description="[STAFF] Mostra o tutorial completo de como colocar um comando customizado.")
    @whitelist_adm_prefix()
    async def admintutorial(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        
        embed = discord.Embed(
            title="Tutorial do bot (STAFF)",
            description="Use os botões para navegar entre os tutoriais.",
            color=discord.Color.dark_gold()
        )

        embed.add_field(name="--- Básico ---", value="- Olá! Hoje o mostrarei todo tutorial do bot na linha da staff, cada página será uma parte do que precisa aprender e saber, cada página dirá muito bem oq eu você precisa saber, principalmente por aqui ser um ''introdutório''.", inline=False)
        embed.add_field(name="", value="- Primeiro de tudo, saiba que caso o bot esteja lento em alguma parte, ele ainda está sob desenvolvimento, então erros podem ser vistos e visíveis, tenha paciência diante do criador do bot.", inline=False)
        embed.set_footer(text="Tutorial (Introdução)  ---  01/05")
        embed.set_image(url="https://tenor.com/kdAaYC1AMNf.gif")
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)


        embed1 = discord.Embed(
            title="Admin Help - Comandos de Administração",
            description="Lista de comandos disponíveis para administradores.",
            color=discord.Color.red()
        )
        if ctx.guild.icon:
            embed1.set_image(url=ctx.guild.icon.url)
        else:
            embed1.set_image(url=None)

        embed1.add_field(name=f"`{prefixo_prefix}helpall`", value="Mostra todos os comandos que precisa saber sobre o bot.", inline=False)
        embed1.add_field(name=f"", value="- Aqui você aprenderá mais do básico com bot.", inline=False)
        embed1.add_field(name=f"", value="- Uma delas é saber quais comandos pode saber, aqui por hora será o básico.", inline=False)
        embed1.set_footer(text="Tutorial (Prefixos/comandos principais)  ---  02/05")
        embed1.set_thumbnail(url=ctx.bot.user.avatar.url)

        embed_tutorial = discord.Embed(
            title="--- Fazendo comando customizado ---",
            description="Aqui será para aprender a como fazer seu comando customizado para seu servidor!",
            color = discord.Color.gold()
        )
    
        embed_tutorial.add_field(name="Baixando o arquivo!", value="- De início, você deve estar pensando... ''Certo, mas como eu crio?'', e eu te respondo de maneira simples.\n\n- Primeiro você executa o comando `/cuscomcommand give <mineração/daily/monster> <quantidade de itens>` e pega o seu molde como preferir com a quantidade de itens, podendo ser 1 que vai ter no arquivo (ex.: mineração ter 7 itens que você vai colocar, etc.), no caso, um desses 2 como exemplo como pode ver na imagem abaixo.", inline=False)
        embed_tutorial.add_field(name="", value="- Após pegar seu arquivo que se encontra em JSON, abra usando um bloco de notas, ou até mesmo copie tudo e mande para um editor de JSON, daí mesmo você pode editar seu comando do jeito como preferir.", inline=False)
        embed_tutorial.add_field(name="", value="(Em caso de dúvidas, o dono recomenda este site (https://jsoneditoronline.org/#left=local.duguyo), ao abrir, só clicar no ícone de pasta, ''open file'' e colocar seu arquivo lá, depois de ditar, só apertar naquele disquete ''salvar'' e com isso, você terá salvado seu arquivo editado, boa edição.)", inline=False)
        embed_tutorial.set_image(url="https://prnt.sc/-B2gm1GZdL2d")
        embed_tutorial.set_footer(text="Tutorial (Baixando o comando customizado)  ---  03/05")
        embed_tutorial.set_thumbnail(url=ctx.bot.user.avatar.url)


        embed_command = discord.Embed(
                            title="--- Adicionando o comando ---",
                            description="Aqui você aprenderá a colocar seu comando, caso não saiba alguma das partes, retorne para entender melhor.",
                            color= discord.Color.dark_green()
        )
        embed_command.add_field(name="Após editar...", value="- Se chegou até aqui, então deve ter seguido bem o tutorial de ter baixado o arquivo e editado usando algum bloco de notaas ou um site, após todo processo dito na página anterior, você vai em algum chat (principalmente de comandos) e digitar `/admin customc add <arquivo>` e envie o arquivo, feito isso, seu comando de mineração caso já esteja setado, já estará funcionando sem medo algum, o mesmo funciona para ''daily''.", inline=False)
        embed_command.add_field(name="Mas e se eu quiser baixar?", value="- Simples, você dá o comando `/admin customc download`, e só deixar salvo consigo, editar algo e afins, mas cuidado, não edite o comando principal, se ele está como `mm-minerar` ou algo do tipo, não altere, ou o bot reconhecerá que é outro comando.", inline=False)
        embed_command.add_field(name="", value="No momento o bot tem `mineração`, `daily`, `???`, breve possa vir mais, por hora, mantenha no aguardo.", inline=False)
        embed_command.set_image(url="https://prnt.sc/wCMHdmB-YjWP")
        embed_command.set_footer(text="Tutorial (Colocando no bot)  ---  04/05")
        embed_command.set_thumbnail(url=ctx.bot.user.avatar.url)



        embed_finish = discord.Embed(
                        title="--- Regras/Conclusão/Últimos ---",
                        description="Aqui vem algumas regras para você ficar por dentro do bot, e conclusão.",
                        color = discord.Color.green()
        )

        embed_finish.add_field(name="Regras:", value="- Não tente adicionar pessoas que não conhece\n- Somente o dono do bot pode adicionar/remover coisas\n- Caso tenha alguma sugestão do que acrescentar, só falar.\n- Divirta-se usando o bot\n- Paciência para caso queira algo (tipo uma forma de ter comandos de pesca), afinal, o dono faz tudo por 1 coisa.\n- E o principal, caso queira editar um comando, edite, mas ***não troque o comando, ou o bot não reconhecerá***.", inline=False)
        embed_finish.add_field(name="Comandos futuros:", value="- Possíveis comandos customizados futuros (dependendo do tempo e do dono):\n\n- `procurado`\n- `pesca`\n- `plantação`\n- `coletagem`\n\n***`E mais outros`***", inline=False)
        embed_finish.add_field(name="", value="- Aviso: Os mesmos comandos que tem em barra (/), também tem para o próprio prefixo do bot, você pode checar no `/admin helpall` para ter uma noção dos comandos.", inline=False)
        embed_finish.add_field(name="''Nossa, mas você fez muitos comandos de help''", value="- Eu sei, proposital para não ter de ficar lembrando sempre de algum comando ou algum help distante para encontraro  que busca. :)", inline=False)
        embed_finish.add_field(name="Whitelist", value="- Isso é coisa somente do dono do bot e/ou do servidor, mas o dono tem capacidade de adicionar qualquer um ou algum cargo na whitelist, ou seja, qualquer pessoa que tenha o nick ou cargo, conseguirá usar o bot, para checar, dê /whitelist.", inline=False)
        embed_finish.add_field(name="DIVIRTA-SE!!!", value="Fim", inline=False)
        embed_finish.set_footer(text="Tutorial (Final)  ---  05/05")
        embed_finish.set_thumbnail(url=ctx.bot.user.avatar.url)
        embed_finish.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwlsklIUZZBHLtj0mfHBx62jGPP3I8GZHX7t3uARp7mfV5vYbsdHc8MUs&s=10")


        lista = [embed, embed1, embed_tutorial, embed_command, embed_finish]
        view = Paginador(paginas=lista)
        await ctx.send(embed=lista[0], view=view)
    





async def setup(bot):
    await bot.add_cog(NormalCommand(bot))