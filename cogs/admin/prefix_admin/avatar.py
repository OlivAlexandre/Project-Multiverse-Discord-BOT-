import discord
from discord.ext import commands
from utils import whitelist_adm_prefix, prefixo
import aiohttp


class avatarBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.group(name="avatar", invoke_without_command=True)
    @whitelist_adm_prefix()
    async def avatar_group(self, ctx):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return

        await ctx.send(f"Especifique a ação: Use `{prefixo_prefix}avatar [set/view]`")

    












    @avatar_group.command(name="set")
    @whitelist_adm_prefix()
    async def avatarset(self, ctx, url: str=None):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return
        
        if ctx.message.attachments:
            imagem_bytes = await ctx.message.attachments[0].read()
        elif url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send(f"Falha ao baixar a imagem. Status: {response.status}")
                        return
                    imagem_bytes = await response.read()

        else:
            await ctx.send(f"Você precisa fornecer uma URL ou anexar uma imagem. Use `{prefixo_prefix}avatar set [URL]` ou anexe uma imagem.")
            return
        
        try:
            await self.bot.user.edit(avatar=imagem_bytes)
            await ctx.send("Avatar do bot atualizado com sucesso!")
        except discord.HTTPException as e:
            await ctx.send(f"Falha ao atualizar o avatar: {e}")
    














    @avatar_group.command(name="view")
    async def avatarview(self, ctx):
        avatar = self.bot.user
        avatar_url = avatar.display_avatar.url
        embed = discord.Embed(
            title="Meu avatar",
            description="Meu avatar atual é este, morra de inveja :3",
            color=discord.Colour.blue()
        )
        if self.bot.user.avatar:
            embed.set_image(url=avatar_url)
        else:
            embed.add_field(name="Aviso", value="Nenhum avatar definido.", inline=False)

        await ctx.send(embed=embed)













    @commands.group(name="banner", invoke_without_command=True)
    @whitelist_adm_prefix()
    async def banner_group(self, ctx):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return

        await ctx.send(f"Especifique a ação: Use `{prefixo_prefix}banner [set/view]`")





    @banner_group.command(name="set")
    @whitelist_adm_prefix()
    async def bannerset(self, ctx, url: str=None):
        prefixo_prefix = await prefixo(self.bot, ctx.message)
        if ctx.guild is None:
            await ctx.send("Esse comando não pode ser usado em mensagens diretas.")
            return
        
        if ctx.message.attachments:
            imagem_bytes = await ctx.message.attachments[0].read()
        elif url:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send(f"Falha ao baixar a imagem. Status: {response.status}")
                        return
                    imagem_bytes = await response.read()

        else:
            await ctx.send(f"Você precisa fornecer uma URL ou anexar uma imagem. Use `{prefixo_prefix}banner set [URL]` ou anexe uma imagem.")
            return
        
        try:
            await self.bot.user.edit(banner=imagem_bytes)
            await ctx.send("Banner do bot atualizado com sucesso!")
        except discord.HTTPException as e:
            await ctx.send(f"Falha ao atualizar o banner: {e}")


    











    @banner_group.command(name="view")
    async def bannerview(self, ctx):
        alvo = self.bot.user
        banner_full = await self.bot.fetch_user(alvo.id)
        

        if not banner_full.banner:
            return await ctx.reply("Ops... não possuo um banner infelizmente! :(", delete_after=10)

        banner_url = banner_full.banner.url

        embed = discord.Embed(
            title="Meu banner",
            description="Meu banner atual é este, só não sinta inveja!!!",
            color=discord.Colour.blue()
        )
        embed.set_image(url=banner_url)

        await ctx.send(embed=embed)





async def setup(bot):
    await bot.add_cog(avatarBot(bot))