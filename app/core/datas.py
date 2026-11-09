"""Funções relacionadas a datas e horários."""

from datetime import datetime, timezone


def agora_utc() -> datetime:
    """Retorna a data e hora atuais com fuso horário UTC."""
    return datetime.now(timezone.utc)