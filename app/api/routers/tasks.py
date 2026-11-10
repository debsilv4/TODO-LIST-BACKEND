
"""Endpoints de tarefas: todos exigem login."""

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import UsuarioAtual, obter_tarefa_servico
from app.schemas import TarefaCreate, TarefaOut
from app.services import TarefaServico

router = APIRouter(
    prefix="/tasks",
    tags=["Tarefas"],
    responses={401: {"description": "Sem token, ou token inválido/expirado"}},
)

Servico = Annotated[TarefaServico, Depends(obter_tarefa_servico)]


@router.post(
    "",
    response_model=TarefaOut,
    status_code=status.HTTP_201_CREATED,
    summary="Criar tarefa",
)
def criar_task(
    dados: TarefaCreate,
    usuario: UsuarioAtual,
    servico: Servico,
) -> TarefaOut:
    return servico.criar(
        usuario_id=usuario.id,
        titulo=dados.titulo,
        prioridade=dados.prioridade,
        prazo=dados.prazo,
    )


@router.get(
    "",
    response_model=list[TarefaOut],
    summary="Listar as tarefas do usuário logado",
)
def listar_tasks(
    usuario: UsuarioAtual,
    servico: Servico,
    response: Response,
) -> list[TarefaOut]:
    tarefas = servico.listar(usuario.id)
    response.headers["X-Total-Count"] = str(len(tarefas))
    return tarefas
