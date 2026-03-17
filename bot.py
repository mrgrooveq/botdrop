# ============================================
# bot.py — Inicialização e eventos principais
# ============================================

import discord
from discord.ext import commands
import logging

from config import TOKEN, GUILD_ID
from data import bot_data
from utils import normalize_answer
from drops import check_expired_roles, handle_winner_dm
from commands import setup_commands

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

setup_commands(bot)

@bot.event
async def on_ready():
    print(f'\n✅ {bot.user} está online!')
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'✅ {len(synced)} comando(s): {[c.name for c in synced]}')
    except Exception as e:
        print(f'❌ Erro ao sincronizar: {e}')
    await check_expired_roles(bot)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Se drops estiverem pausados, ignora qualquer resposta
    if bot_data.drops_paused:
        await bot.process_commands(message)
        return

    if (bot_data.drop_active and
        message.channel.id == bot_data.drop_channel_id and
        message.author.id not in bot_data.answered_users):

        if any(normalize_answer(message.content) == c for c in bot_data.current_answers):
            bot_data.drop_active = False
            bot_data.answered_users.add(message.author.id)
            bot_data.save_data()

            await message.channel.send(
                embed=discord.Embed(
                    description=(
                        f"# 🎆 Temos um vencedor!\n\n"
                        f"Parabéns {message.author.mention}! Você acertou a resposta e ganhou o drop! "
                        f"Verifique suas DMs para escolher seu prêmio."
                    ),
                    color=discord.Color.gold()
                ),
                allowed_mentions=discord.AllowedMentions(users=True)
            )

            await handle_winner_dm(bot, message)

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(TOKEN)