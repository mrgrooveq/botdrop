# ============================================
# drops.py — Lógica de envio e controle dos drops
# ============================================

import discord
import asyncio
from datetime import datetime, timedelta

from config import TEMPORARY_ROLES, ROLE_NAMES, DROP_CHANNEL_ID, GUILD_ID
from data import bot_data
from utils import normalize_answer

async def send_drop(channel: discord.TextChannel, question_text: str, answers_list: list):
    if bot_data.drops_paused:
        print("⏸️ Drops estão pausados, ignorando chamada.")
        return

    bot_data.current_question = question_text
    bot_data.current_answers = [normalize_answer(a) for a in answers_list]
    bot_data.drop_active = True
    bot_data.drop_channel_id = channel.id
    bot_data.answered_users = set()
    bot_data.last_drop_time = datetime.now().isoformat()
    bot_data.save_data()

    embed = discord.Embed(
        description=(
            f"# 🎁 DROP RÁPIDO!\n"
            f"-# **{bot_data.current_question}**\n"
            f"\n"
            f"Responda no chat em até **2 minutos** para ganhar um cargo\n"
            f"(Cam 10, Capitão, Perm. Amistosos ou Perm. Drops)"
        ),
        color=discord.Color.gold()
    )
    embed.set_footer(text="Spider TEAM")
    await channel.send("@here", embed=embed)

    await asyncio.sleep(120)

    if bot_data.drop_active:
        resposta = bot_data.current_answers[0] if bot_data.current_answers else "?"
        bot_data.drop_active = False
        bot_data.save_data()
        await channel.send(embed=discord.Embed(
            title="Tempo Esgotado!",
            description=f"Ninguém acertou o drop desta vez. A resposta era: **{resposta}**",
            color=discord.Color.red()
        ))

async def assign_temporary_role(bot: discord.Client, user_id: int, role_id: int):
    if not role_id:
        print("❌ role_id é None")
        return False
    try:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            print("❌ Servidor não encontrado")
            return False
        member = guild.get_member(user_id)
        if not member:
            member = await guild.fetch_member(user_id)
        if not member:
            print(f"❌ Membro {user_id} não encontrado")
            return False
        role = guild.get_role(role_id)
        if not role:
            print(f"❌ Cargo {role_id} não encontrado")
            return False
        await member.add_roles(role)
        bot_data.winners[str(user_id)] = (datetime.now() + timedelta(days=5)).isoformat()
        bot_data.save_data()
        print(f"✅ Cargo {role.name} atribuído para {member.name}")
        return True
    except Exception as e:
        print(f"❌ Erro ao atribuir cargo: {e}")
        return False

async def check_expired_roles(bot: discord.Client):
    current_time = datetime.now()
    expired_users = []
    for user_id, expiry_str in list(bot_data.winners.items()):
        try:
            if current_time > datetime.fromisoformat(expiry_str):
                expired_users.append(int(user_id))
        except:
            continue
    for user_id in expired_users:
        guild = bot.get_guild(GUILD_ID)
        if not guild:
            continue
        member = guild.get_member(user_id)
        if member:
            for role_id in TEMPORARY_ROLES.values():
                if role_id:
                    role = guild.get_role(role_id)
                    if role and role in member.roles:
                        await member.remove_roles(role)
            bot_data.winners.pop(str(user_id), None)
            bot_data.save_data()
            try:
                await member.send("⏰ **Seu cargo temporário de 5 dias expirou!**")
            except:
                pass

async def handle_winner_dm(bot: discord.Client, message: discord.Message):
    if not any(v for v in TEMPORARY_ROLES.values()):
        print("⚠️ Nenhum cargo configurado, pulando DM.")
        return

    try:
        dm = await message.author.create_dm()

        roles_list = "\n".join(
            f"`{k}` — {ROLE_NAMES[k]}"
            for k, v in TEMPORARY_ROLES.items() if v
        )

        await dm.send(embed=discord.Embed(
            title="🎁 VOCÊ GANHOU!",
            description=(
                f"Parabéns, **{message.author.name}**!\n\n"
                f"**Escolha seu prêmio digitando o número:**\n\n"
                f"{roles_list}\n\n"
                f"`0` — Já tenho todos esses cargos."
            ),
            color=discord.Color.gold()
        ).set_footer(text="Você tem 2 minutos. Digite o número do prêmio ou 0."))

        print(f"✅ DM enviada para {message.author.name}")

        valid = [k for k, v in TEMPORARY_ROLES.items() if v]

        def check(m):
            return (m.author.id == message.author.id
                    and isinstance(m.channel, discord.DMChannel)
                    and (m.content in valid or m.content == "0"))

        try:
            msg = await bot.wait_for('message', timeout=120.0, check=check)

            if msg.content == "0":
                await dm.send(embed=discord.Embed(
                    title="Tudo bem!",
                    description="Sem problemas. Parabéns pela vitória mesmo assim! 🏆",
                    color=discord.Color.blurple()
                ))
                return

            role_id = TEMPORARY_ROLES[msg.content]
            role_name = ROLE_NAMES[msg.content]

            if await assign_temporary_role(bot, message.author.id, role_id):
                await dm.send(embed=discord.Embed(
                    title="✅ Prêmio Atribuído!",
                    description=f"Você recebeu o cargo **{role_name}** por **5 dias**!",
                    color=discord.Color.green()
                ))
            else:
                await dm.send("❌ Erro ao atribuir o prêmio. Contate um admin.")

        except asyncio.TimeoutError:
            await dm.send(embed=discord.Embed(
                title="⏰ Tempo Esgotado",
                description="Você demorou e perdeu a chance de escolher.",
                color=discord.Color.red()
            ))

    except discord.Forbidden:
        print(f"❌ DM bloqueada para {message.author.name}")
        await message.channel.send(
            f"{message.author.mention} ❌ Não consegui te enviar DM! "
            f"Ative as mensagens diretas do servidor para receber seu prêmio.",
            allowed_mentions=discord.AllowedMentions(users=True)
        )