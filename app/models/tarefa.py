
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, validates

from app.core.datas import agora_utc
from app.core.exceptions import TituloObrigatorio, ValorInvalido
from app.db.database import Base
from app.models.enums import PrioridadeTarefa, StatusTarefa


class Tarefa(Base):
    """Entidade Tarefa: dados e regras de uma tarefa."""

    __tablename__ = "tarefas"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(
        Integer, ForeignKey("usuarios.id"), nullable=False, index=True
    )

    titulo = Column(String(200), nullable=False)

    _status = Column("status", String(20), nullable=False)
    prioridade = Column(String(20), nullable=False)
    prazo = Column(Date, nullable=True)

    criado_em = Column(
        DateTime(timezone=True), nullable=False, default=agora_utc
    )

    atualizado_em = Column(
        DateTime(timezone=True),
        nullable=False,
        default=agora_utc,
        onupdate=agora_utc,
    )

    _concluido_em = Column(
        "concluido_em", DateTime(timezone=True), nullable=True
    )

    usuario = relationship("Usuario", back_populates="tarefas")

    def __init__(
        self,
        *,
        usuario_id: int,
        titulo: str,
        prioridade: PrioridadeTarefa | str = PrioridadeTarefa.MEDIA,
        prazo: date | None = None,
    ) -> None:
        """Cria uma tarefa inicialmente pendente."""

        self.usuario_id = usuario_id
        self.titulo = titulo
        self.prioridade = prioridade
        self.prazo = prazo
        self._status = StatusTarefa.PENDENTE.value
        self._concluido_em = None

    @property
    def status(self) -> StatusTarefa:
        """Retorna o status atual da tarefa."""
        return StatusTarefa(self._status)

    @property
    def concluido_em(self) -> datetime | None:
        """Retorna a data de conclusão da tarefa."""
        return self._concluido_em

    def pertence_a(self, usuario_id: int) -> bool:
        """Verifica se a tarefa pertence ao usuário."""
        return self.usuario_id == usuario_id

    @validates("titulo")
    def validar_titulo(self, _campo: str, valor: str) -> str:
        """Impede títulos vazios."""
        if valor is None or not valor.strip():
            raise TituloObrigatorio()

        return valor.strip()

    @validates("prioridade")
    def validar_prioridade(self, _campo: str, valor: object) -> str:
        """Valida e converte a prioridade."""
        try:
            return PrioridadeTarefa(valor).value
        except ValueError as err:
            permitidos = ", ".join(p.value for p in PrioridadeTarefa)

            raise ValorInvalido(
                f"Prioridade inválida. Valores aceitos: {permitidos}."
            ) from err

    def __repr__(self) -> str:
        return (
            f"<Tarefa id={self.id} titulo={self.titulo!r} "
            f"status={self._status!r}>"
        )
