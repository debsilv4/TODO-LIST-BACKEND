
"""Modelo de usuário armazenado no banco de dados."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.datas import agora_utc
from app.core.exceptions import ValorInvalido
from app.core.security import HashDeSenha
from app.db.database import Base


class Usuario(Base):
    """Representa um usuário da aplicação."""

    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(180),
        unique=True,
        index=True,
        nullable=False,
    )

    _senha_hash: Mapped[str] = mapped_column(
        "senha_hash",
        String(255),
        nullable=False,
    )

    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=agora_utc,
        nullable=False,
    )

    tarefas: Mapped[list["Tarefa"]] = relationship(
        "Tarefa",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    def __init__(self, *, nome: str, email: str) -> None:
        self.nome = nome.strip()
        self.email = self.normalizar_email(email)

    @staticmethod
    def normalizar_email(email: str) -> str:
        """Padroniza o e-mail."""
        return email.strip().lower()

    def definir_senha(self, senha: str, hasher: HashDeSenha) -> None:
        """Armazena a senha em formato hash."""
        self._senha_hash = hasher.gerar(senha)

    def senha_confere(self, senha: str, hasher: HashDeSenha) -> bool:
        """Confere se a senha está correta."""
        return hasher.verificar(senha, self._senha_hash)

    @validates("nome")
    def _validar_nome(self, _campo: str, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValorInvalido("O nome do usuário não pode ficar vazio.")
        return valor.strip()

    def __repr__(self) -> str:
        return f"Usuario(id={self.id!r}, email={self.email!r})"
