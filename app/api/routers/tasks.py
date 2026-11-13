
"""Endpoints de tarefas: todos exigem login."""

from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from app.api.dependencies import UsuarioAtual, obter_tarefa_servico
from app.schemas import TarefaCreate, TarefaUpdate, TarefaOut
from app.services.tarefa import TarefaServico, AlteracoesDaTarefa

router = APIRouter(
    prefix="/tasks",
    tags=["Tarefas"],
    responses={
        401: {"description": "Sem token ou token inválido/expirado"},
    },
)

Servico = Annotated[
    TarefaServico,
    Depends(obter_tarefa_servico),
]


def _montar_alteracoes(
    dados: TarefaUpdate,
) -> AlteracoesDaTarefa:
    """Converte os dados do PATCH em alterações."""
    return AlteracoesDaTarefa(
        **dados.model_dump(exclude_unset=True)
    )


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
    summary="Listar tarefas do usuário logado",
)
def listar_tasks(
    usuario: UsuarioAtual,
    servico: Servico,
    response: Response,
) -> list[TarefaOut]:
    tarefas = servico.listar(usuario.id)
    response.headers["X-Total-Count"] = str(len(tarefas))
    return tarefas


@router.get(
    "/{tarefa_id}",
    response_model=TarefaOut,
    summary="Buscar tarefa pelo ID",
    responses={
        403: {"description": "A tarefa pertence a outro usuário"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def buscar_task(
    tarefa_id: int,
    usuario: UsuarioAtual,
    servico: Servico,
) -> TarefaOut:
    return servico.buscar(
        tarefa_id=tarefa_id,
        usuario_id=usuario.id,
    )


@router.patch(
    "/{tarefa_id}",
    response_model=TarefaOut,
    summary="Atualizar uma tarefa",
    responses={
        403: {"description": "A tarefa pertence a outro usuário"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def atualizar_task(
    tarefa_id: int, dados: TarefaUpdate, usuario: UsuarioAtual, servico: Servico
) -> TarefaOut:
    alteracoes = _montar_alteracoes(dados)

    return servico.atualizar(
        tarefa_id=tarefa_id,
        usuario_id=usuario.id,
        alteracoes=alteracoes,
    )


@router.delete(
    "/{tarefa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir uma tarefa",
    responses={
        403: {"description": "A tarefa pertence a outro usuário"},
        404: {"description": "Tarefa não encontrada"},
    },
)
def remover_task(
    tarefa_id: int,
    usuario: UsuarioAtual,
    servico: Servico,
) -> Response:
    servico.remover(
        tarefa_id=tarefa_id,
        usuario_id=usuario.id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
