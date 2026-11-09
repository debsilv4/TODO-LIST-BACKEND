"""Repositório de usuários.

RN-01: um e-mail não pode ser usado por dois usuários.
"""

from sqlalchemy import select

from app.models.usuario import Usuario
from app.repositories.base import RepositorioBase


class UsuarioRepositorio(RepositorioBase[Usuario]):
    """Realiza consultas e gravações de usuários."""

    @property
    def modelo(self) -> type[Usuario]:
        return Usuario

    def buscar_por_id(self, identificador: int) -> Usuario | None:
        return self.sessao.get(Usuario, identificador)

    def buscar_por_email(self, email: str) -> Usuario | None:
        consulta = select(Usuario).where(
            Usuario.email == Usuario.normalizar_email(email)
        )

        return self.sessao.scalar(consulta)

    def email_existe(self, email: str) -> bool:
        """Verifica se o e-mail já está cadastrado conforme a RN-01."""
        return self.buscar_por_email(email) is not None