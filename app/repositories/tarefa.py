
"""Acesso aos dados de tarefa."""

from __future__ import annotations

from app.models import Tarefa
from app.repositories.base import RepositorioBase


class TarefaRepositorio(RepositorioBase[Tarefa]):
    """Acesso aos dados de tarefa."""

    @property
    def modelo(self) -> type[Tarefa]:
        return Tarefa

    def buscar_por_id(self, identificador: int) -> Tarefa | None:
        """Busca uma tarefa pelo seu identificador."""
        return self.sessao.get(Tarefa, identificador)

    def listar(self, usuario_id: int) -> list[Tarefa]:
        """Lista as tarefas de um usuário."""

        return (
            self.sessao.query(Tarefa)
            .filter(Tarefa.usuario_id == usuario_id)
            .order_by(Tarefa.criado_em.desc(), Tarefa.id.desc())
            .all()
        )
