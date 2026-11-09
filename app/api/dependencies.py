<<<<<<< HEAD
"""Provedores de dependência: montam os objetos que as rotas usam.

Concentrar a montagem aqui tem um efeito prático: a rota declara que precisa
de um `TarefaServico` e não sabe quantas peças existem por trás dele. Se
amanhã o serviço passar a receber um colaborador novo, muda este módulo - e
nenhuma rota.
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

=======
"""Provedores de dependência: montam os objetos que as rotas usam."""
from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
from app.core.config import obter_configuracao
from app.core.exceptions import NaoAutenticado
from app.core.security import HashBcrypt, HashDeSenha, TokenJWT
from app.db.database import obter_sessao
from app.models import Usuario
<<<<<<< HEAD
from app.repositories import TarefaRepositorio, UsuarioRepositorio
from app.services import TarefaServico, UsuarioServico

_esquema_bearer = HTTPBearer(auto_error=False, description="Token recebido no login")


def obter_hasher() -> HashDeSenha:
    """Implementação de hash usada pela aplicação."""
    return HashBcrypt()


=======
from app.repositories import UsuarioRepositorio
from app.services import UsuarioServico
_esquema_bearer = HTTPBearer(auto_error=False, description="Token recebido no login")
def obter_hasher() -> HashDeSenha:
    """Implementação de hash usada pela aplicação."""
    return HashBcrypt()
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
def obter_tokens() -> TokenJWT:
    """Emissor/leitor de tokens, com o segredo e a validade da configuração."""
    config = obter_configuracao()
    return TokenJWT(config.segredo_jwt(), config.jwt_expira_minutos)
<<<<<<< HEAD


=======
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
def obter_usuario_servico(
    sessao: Session = Depends(obter_sessao),
    hasher: HashDeSenha = Depends(obter_hasher),
    tokens: TokenJWT = Depends(obter_tokens),
) -> UsuarioServico:
    """Serviço de usuários, com repositório, hasher e tokens já injetados."""
    return UsuarioServico(UsuarioRepositorio(sessao), hasher, tokens)
<<<<<<< HEAD


def obter_tarefa_servico(
    sessao: Session = Depends(obter_sessao),
) -> TarefaServico:
    """Serviço de tarefas, com o repositório de que depende."""
    return TarefaServico(TarefaRepositorio(sessao))


def obter_usuario_atual(
    credenciais: Annotated[
=======
def obter_usuario_atual(
    credenciais:Annotated[
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
        HTTPAuthorizationCredentials | None, Depends(_esquema_bearer)
    ],
    servico: Annotated[UsuarioServico, Depends(obter_usuario_servico)],
) -> Usuario:
<<<<<<< HEAD
    """Identifica quem está fazendo a requisição, a partir do token."""
    if credenciais is None:
        raise NaoAutenticado()
    return servico.usuario_do_token(credenciais.credentials)


# Atalho legível para as rotas: `usuario: UsuarioAtual`.
UsuarioAtual = Annotated[Usuario, Depends(obter_usuario_atual)]
=======
    """Identifica quem está fazendo a requisição, a partir do token. """
    if credenciais is None:
        raise NaoAutenticado()
    return servico.usuario_do_token(credenciais.credentials)
UsuarioAtual = Annotated[Usuario, Depends(obter_usuario_atual)]
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
