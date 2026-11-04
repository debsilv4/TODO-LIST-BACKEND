"""Esquemas base de validação da API."""

from datetime import datetime, timezone
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


def _garantir_utc(valor: datetime) -> datetime:
    """Garante que a data tenha fuso horário UTC."""
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)

    return valor.astimezone(timezone.utc)


DataHoraUTC = Annotated[datetime, AfterValidator(_garantir_utc)]


class EsquemaDeEntrada(BaseModel):
    """Configuração compartilhada pelos esquemas de entrada."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class EsquemaDeSaida(EsquemaDeEntrada):
    """Configuração compartilhada pelos esquemas de resposta."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )