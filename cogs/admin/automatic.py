import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import discord
from discord import app_commands
from discord.ext import commands, tasks
from cogs.admin.motor import process_command


timezone = ZoneInfo("America/Sao_Paulo")


class automaticMotor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.verificador.start()

    def cog_unload(self):
        self.verificador.cancel()
    

    @tasks.loop(minutes=1)
    async def verificador(self):

        now = datetime.now(timezone)
        hora_atual = now.strftime("%H:%M")
        hora_hoje = now.strftime("%Y-%m-%d")


        conn = sqlite3.connect("json.db")
        cursor = conn.cursor()


        cursor.execute("SELECT id, canal_id, nome_comando, tipo, tempo, ultima_execucao, role_id FROM automatico")
        works = cursor.fetchall()

        for id_tarefa, canal_id, nome_comando, tipo, tempo, ultima_execucao, role_id in works:
            executar = False
        
            if tipo == "diario":
                if hora_atual == tempo:
                    if not ultima_execucao or not ultima_execucao.startswith(hora_hoje):
                        executar = True
            
            elif tipo == "intervalo":
                try:
                    intervalo_min = int(tempo)
                except ValueError:
                    print(f"[ERROR] Valor inválido para intervalo: {tempo}")
                    continue

                if not ultima_execucao:
                    executar = True
                else:
                    try:
                        ultima_dt = datetime.fromisoformat(ultima_execucao)

                        if ultima_dt.tzinfo is None:
                            ultima_dt = ultima_dt.replace(tzinfo=timezone)
                        else:
                            ultima_dt = ultima_dt.astimezone(timezone)

                        if (now - ultima_dt) >= timedelta(minutes=intervalo_min):
                            executar = True
                    except Exception as e:
                        print(f"[ERROR] Falha ao processar ultima_execucao: {ultima_execucao}, motivo: {e}")
                        executar = False
            
            if executar:
                canal = self.bot.get_channel(canal_id)
                if not canal:
                    try:
                        canal = await self.bot.fetch_channel(canal_id)
                    except Exception as e:
                        print(f"[ERROR] Falha ao buscar canal com ID {canal_id}: {e}")
                        continue

                if canal:
                    sucesso = False
                    nome_cmd_limpo = nome_comando.lower().strip()

                    nativo = self.bot.get_command(nome_cmd_limpo)
                    if nativo is not None:
                        try:
                            ctx = await self.bot.get_context(
                                await canal.send(f"Executando comando automático: `{nome_cmd_limpo}`")
                            )
                            await nativo.invoke(ctx)
                            sucesso = True
                        except Exception as err_cmd:
                            print(f"[ERROR] Erro ao rodar comando nativo, motivo:\n\nR - {err_cmd}")
                    else:
                        try:
                            cargo = canal.guild.get_role(role_id) if role_id else None
                            res = await process_command(
                                            bot=self.bot, 
                                            mensagem=None, 
                                            canal=canal, 
                                            guild_id=canal.guild.id, 
                                            author=self.bot.user, 
                                            nome_comando=nome_cmd_limpo, 
                                            ping=cargo)
                            sucesso = True if res is None else bool(res)
                        except Exception as err_cmd:
                            print(f"[ERROR] Erro ao rodar comando customizado, motivo:\n\nR - {err_cmd}\n----------------")
                        
                    if sucesso:
                        cursor.execute("UPDATE automatico SET ultima_execucao = ? WHERE id = ?",
                                        (now.isoformat(), id_tarefa))
                        conn.commit()
                        




    @verificador.before_loop
    async def before_loop(self):
        await self.bot.wait_until_ready()

        

async def setup(bot):
    await bot.add_cog(automaticMotor(bot))