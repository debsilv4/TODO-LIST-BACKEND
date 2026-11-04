"""Schemas Pydantic: o contrato de entrada e saída da API.

Aqui mora a tradução entre dois mundos se nomeclatura. o Python escreve
`criado_em`; o JSON ue o front-end consome espera `criadoEm`. A conversão
acontece **na borda**, que é o lugar dela: o domínio fala Python idíomatico e
estes schemas fazem a tradução automaticamnte, pelo `alias_generator´.
`populate_by_name=True´ mantém a compatibilidade: a API aceita tanto o nome em
camelCase quanto o nome em Python na entrada.
"""

from app.schemas.base import (
    DataHoraUTC,
    EsquemaDeEntrada,
    EsquemaDeSaida,
)
from app.schemas.usuario import SessaoOut, UsuarioCreate, UsuarioLogin, UsuarioOut

__all__ = [
    "DataHoraUTC",
    "EsquemaDeEntrada",
    "EsquemaDeSaida",
    "UsuarioCreate",
    "UsuarioOut",
]