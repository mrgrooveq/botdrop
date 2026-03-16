# ============================================
# commands.py — Slash Commands
# ============================================

import discord
from discord import app_commands
from datetime import datetime

from config import GUILD_ID, DROP_COOLDOWN, DROP_CHANNEL_ID, TEMPORARY_ROLES, ROLE_NAMES
from data import bot_data
from utils import has_authorized_role
from drops import send_drop

def setup_commands(bot: discord.Client):

    # ── /startdrop ──────────────────────────────────────
    @bot.tree.command(
        name="startdrop",
        description="Inicia um drop com pergunta e resposta personalizadas.",
        guild=discord.Object(id=GUILD_ID)
    )
    @app_commands.describe(
        pergunta="A pergunta que aparecerá no drop.",
        resposta="A resposta correta da pergunta."
    )
    async def startdrop(interaction: discord.Interaction, pergunta: str, resposta: str):
        if not has_authorized_role(interaction.user):
            await interaction.response.send_message("❌ Você não tem permissão!", ephemeral=True)
            return
        if bot_data.drop_active:
            await interaction.response.send_message("❌ Já existe um drop ativo!", ephemeral=True)
            return
        if bot_data.last_drop_time:
            diff = (datetime.now() - datetime.fromisoformat(bot_data.last_drop_time)).total_seconds()
            if diff < DROP_COOLDOWN:
                remaining = int(DROP_COOLDOWN - diff)
                await interaction.response.send_message(
                    f"⏳ Aguarde **{remaining}s** antes de iniciar outro drop!", ephemeral=True
                )
                return

        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send("✅ Drop iniciado!", ephemeral=True)
        await send_drop(interaction.channel, pergunta, [resposta])

    # ── /stopdrop ───────────────────────────────────────
    @bot.tree.command(
        name="stopdrop",
        description="Para o drop ativo.",
        guild=discord.Object(id=GUILD_ID)
    )
    async def stopdrop(interaction: discord.Interaction):
        if not has_authorized_role(interaction.user):
            await interaction.response.send_message("❌ Você não tem permissão!", ephemeral=True)
            return
        if not bot_data.drop_active:
            await interaction.response.send_message("ℹ️ Nenhum drop está ativo no momento.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)
        bot_data.drop_active = False
        bot_data.save_data()
        await interaction.followup.send("🛑 Drop encerrado!", ephemeral=True)

        channel = bot.get_channel(DROP_CHANNEL_ID)
        if channel:
            await channel.send(embed=discord.Embed(
                title="Drop Encerrado!",
                description="O drop foi encerrado por um administrador.",
                color=discord.Color.red()
            ))

    # ── /cargosdrops ────────────────────────────────────
    @bot.tree.command(
        name="cargosdrops",
        description="Configura os cargos dos prêmios do drop.",
        guild=discord.Object(id=GUILD_ID)
    )
    async def cargosdrops(interaction: discord.Interaction):
        if not has_authorized_role(interaction.user):
            await interaction.response.send_message("❌ Você não tem permissão!", ephemeral=True)
            return

        def build_embed():
            embed = discord.Embed(
                title="⚙️ Configuração de Cargos",
                description="Clique em um botão para alterar o cargo do prêmio correspondente.",
                color=discord.Color.blurple()
            )
            for k in TEMPORARY_ROLES:
                role_id = TEMPORARY_ROLES[k]
                name = ROLE_NAMES[k]
                if role_id:
                    role = interaction.guild.get_role(role_id)
                    value = role.mention if role else f"⚠️ ID inválido: `{role_id}`"
                else:
                    value = "❌ Não configurado"
                embed.add_field(name=f"Prêmio {k} — {name}", value=value, inline=False)
            embed.set_footer(text="Apenas você pode ver e interagir com este painel.")
            return embed

        class CargoButton(discord.ui.Button):
            def __init__(self, slot: str):
                self.slot = slot
                super().__init__(
                    label=f"Alterar Prêmio {slot} ({ROLE_NAMES[slot]})",
                    style=discord.ButtonStyle.secondary
                )

            async def callback(self, btn_interaction: discord.Interaction):
                if btn_interaction.user.id != interaction.user.id:
                    await btn_interaction.response.send_message("❌ Apenas quem usou o comando pode interagir.", ephemeral=True)
                    return

                await btn_interaction.response.send_message(
                    f"Digite o **ID** ou **mencione** o cargo para o **Prêmio {self.slot}** ({ROLE_NAMES[self.slot]}):\n"
                    f"-# Você tem 30 segundos.",
                    ephemeral=True
                )

                def msg_check(m):
                    return m.author.id == interaction.user.id and m.channel.id == interaction.channel.id

                try:
                    msg = await bot.wait_for('message', timeout=30.0, check=msg_check)

                    role = None
                    if msg.role_mentions:
                        role = msg.role_mentions[0]
                    else:
                        try:
                            role = interaction.guild.get_role(int(msg.content.strip()))
                        except ValueError:
                            pass

                    try:
                        await msg.delete()
                    except:
                        pass

                    if role:
                        TEMPORARY_ROLES[self.slot] = role.id
                        ROLE_NAMES[self.slot] = role.name
                        await btn_interaction.edit_original_response(
                            content=f"✅ Prêmio **{self.slot}** atualizado para **{role.name}**!"
                        )
                        await interaction.edit_original_response(embed=build_embed(), view=view)
                    else:
                        await btn_interaction.edit_original_response(
                            content="❌ Cargo não encontrado. Use o ID ou mencione com @cargo."
                        )

                except Exception:
                    await btn_interaction.edit_original_response(content="⏰ Tempo esgotado. Tente novamente.")

        class CargosView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=120)
                for k in TEMPORARY_ROLES:
                    self.add_item(CargoButton(k))

            async def on_timeout(self):
                try:
                    for item in self.children:
                        item.disabled = True
                    await interaction.edit_original_response(view=self)
                except:
                    pass

        view = CargosView()
        await interaction.response.defer(ephemeral=True)
        await interaction.followup.send(embed=build_embed(), view=view, ephemeral=True)