
"""Acesso aos dados de tarefa."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy import case

from app.models.tarefa import Tarefa
from app.models.enums import (
    CampoOrdenacao,
    Ordem,
    PrioridadeTarefa,
    StatusTarefa,
)
from app.repositories.base import RepositorioBase


@dataclass(frozen=True)
class FiltroDeTarefas:
    """Critérios de uma consulta de tarefa."""

    usuario_id: int
    status: StatusTarefa | None = None
    prioridade: PrioridadeTarefa | None = None
    prazo_ate: date | None = None
    busca: str | None = None
    ordenar_por: CampoOrdenacao = CampoOrdenacao.CRIADO_EM
    ordem: Ordem = Ordem.DESC
    limite: int = 100
    deslocamento: int = 0


@dataclass(frozen=True)
class PaginaDeTarefas:
    """Resultado paginado de uma consulta."""

    tarefas: list[Tarefa]
    total: int


class TarefaRepositorio(RepositorioBase[Tarefa]):
    """Acesso aos dados de tarefa."""

    _ORDEM_POR_PRIORIDADE = case(
        PrioridadeTarefa.mapa_de_pesos(),
        value=Tarefa.prioridade,
        else_=99,
    )

    @property
    def modelo(self) -> type[Tarefa]:
        return Tarefa

    def buscar_por_id(self, identificador: int) -> Tarefa | None:
        """Busca uma tarefa pelo identificador."""

        return (
            self.sessao.query(self.modelo)
            .filter(self.modelo.id == identificador)
            .first()
        )

    def _coluna_de_ordenacao(self, campo: CampoOrdenacao):
        colunas = {
            CampoOrdenacao.CRIADO_EM: Tarefa.criado_em,
            CampoOrdenacao.PRAZO: Tarefa.prazo,
            CampoOrdenacao.PRIORIDADE: self._ORDEM_POR_PRIORIDADE,
        }

        return colunas[campo]

    def listar(self, filtro: FiltroDeTarefas) -> PaginaDeTarefas:
        """Lista as tarefas de um usuário conforme os critérios informados."""

        consulta = self.sessao.query(Tarefa).filter(
            Tarefa.usuario_id == filtro.usuario_id
        )

        if filtro.status is not None:
            consulta = consulta.filter(
                Tarefa.status == filtro.status.value
            )

        if filtro.prioridade is not None:
            consulta = consulta.filter(
                Tarefa.prioridade == filtro.prioridade.value
            )

        if filtro.prazo_ate is not None:
            consulta = consulta.filter(
                Tarefa.prazo.isnot(None),
                Tarefa.prazo <= filtro.prazo_ate,
            )

        if filtro.busca:
            consulta = consulta.filter(
                Tarefa.titulo.icontains(
                    filtro.busca,
                    autoescape=True,
                )
            )

        total = consulta.order_by(None).count()

        coluna = self._coluna_de_ordenacao(filtro.ordenar_por)

        ordenacao = [
            coluna.desc()
            if filtro.ordem is Ordem.DESC
            else coluna.asc()
        ]

        if filtro.ordenar_por is CampoOrdenacao.PRAZO:
            ordenacao.insert(
                0,
                case((Tarefa.prazo.is_(None), 1), else_=0),
            )

        ordenacao.append(Tarefa.id.desc())

        tarefas = (
            consulta.order_by(*ordenacao)
            .offset(filtro.deslocamento)
            .limit(filtro.limite)
            .all()
        )

        return PaginaDeTarefas(
            tarefas=tarefas,
            total=total,
        )

    def todas_do_usuario(self, usuario_id: int) -> list[Tarefa]:
        """Retorna todas as tarefas de um usuário."""

        return (
            self.sessao.query(Tarefa)
            .filter(Tarefa.usuario_id == usuario_id)
            .all()
        )
