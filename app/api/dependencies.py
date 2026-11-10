
"""Dependências da API para injeção no FastAPI."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.exceptions import NaoAutenticado, TokenInvalido
from app.core.config import obter_configuracao
from app.core.security import HashBcrypt, TokenJWT
from app.db.database import obter_sessao
from app.models import Usuario
from app.repositories import UsuarioRepositorio, TarefaRepositorio
from app.services.usuario import UsuarioServico
from app.services.tarefa import TarefaServico


bearer = HTTPBearer(auto_error=False)


def obter_usuario_servico(
    sessao: Annotated[Session, Depends(obter_sessao)]
) -> UsuarioServico:

    configuracao = obter_configuracao()

    repositorio = UsuarioRepositorio(sessao)
    hasher = HashBcrypt()

    tokens = TokenJWT(
        segredo=configuracao.segredo_jwt(),
        expira_minutos=configuracao.jwt_expira_minutos,
    )

    return UsuarioServico(
        repositorio=repositorio,
        hasher=hasher,
        tokens=tokens,
    )


def obter_tarefa_servico(
    sessao: Annotated[Session, Depends(obter_sessao)]
) -> TarefaServico:

    repositorio = TarefaRepositorio(sessao)

    return TarefaServico(repositorio)


def obter_usuario_atual(
    credenciais: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer)
    ],
    servico: Annotated[
        UsuarioServico,
        Depends(obter_usuario_servico)
    ],
) -> Usuario:

    if credenciais is None:
        raise NaoAutenticado("Token de acesso ausente.")

    token = credenciais.credentials

    try:
        return servico.usuario_do_token(token)
    except TokenInvalido:
        raise
    except Exception as erro:
        raise TokenInvalido() from erro


UsuarioAtual = Annotated[
    Usuario,
    Depends(obter_usuario_atual)
]
