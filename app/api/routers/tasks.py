
"""Endpoints de tarefas: todos exigem login."""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.dependencies import UsuarioAtual, obter_tarefa_servico
from app.schemas import ResumoOut, TarefaCreate, TarefaUpdate, TarefaOut
from app.services import TarefaServico
from app.services.tarefa import AlteracoesDaTarefa
from app.repositories import FiltroDeTarefas
from app.models.enums import (
    CampoOrdenacao,
    Ordem,
    PrioridadeTarefa,
    StatusTarefa,
)


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
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    status: StatusTarefa | None = None,
    prioridade: PrioridadeTarefa | None = None,
    prazo_ate: date | None = None,
    busca: str | None = None,
    ordenar_por: CampoOrdenacao = CampoOrdenacao.CRIADO_EM,
    ordem: Ordem = Ordem.DESC,
) -> list[TarefaOut]:

    filtro = FiltroDeTarefas(
        usuario_id=usuario.id,
        status=status,
        prioridade=prioridade,
        prazo_ate=prazo_ate,
        busca=busca,
        ordenar_por=ordenar_por,
        ordem=ordem,
        limite=limit,
        deslocamento=offset,
    )

    pagina = servico.listar(filtro)

    response.headers["X-Total-Count"] = str(pagina.total)

    return pagina.tarefas


@router.get(
    "/resumo",
    response_model=ResumoOut,
    summary="Resumo para o Painel",
)
def resumo_tasks(
    usuario: UsuarioAtual,
    servico: Servico,
) -> ResumoOut:
    return servico.resumo(usuario.id)


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
    tarefa_id: int,
    dados: TarefaUpdate,
    usuario: UsuarioAtual,
    servico: Servico,
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
