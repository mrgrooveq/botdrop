# ============================================
# utils.py — Funções auxiliares
# ============================================

import re
import unicodedata
import discord
from config import AUTHORIZED_ROLES

def normalize_answer(text: str) -> str:
    """Remove acentos, pontuação, espaços extras e coloca em minúsculo.
    Permite que 'Atlético de Madrid' == 'atletico de madrid'."""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return text

def has_authorized_role(member: discord.Member) -> bool:
    """Verifica se o membro tem algum cargo autorizado."""
    return any(role.id in AUTHORIZED_ROLES for role in member.roles)