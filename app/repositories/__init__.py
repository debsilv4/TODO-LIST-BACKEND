<<<<<<< HEAD
"""Repositórios: a única camada que conversa com o banco de dados.

A regra é: serviço não sabe SQL, rota não sabe banco. Quem precisa de dados
pede a um repositório.
"""

from app.repositories.base import RepositorioBase
from app.repositories.tarefa import TarefaRepositorio
from app.repositories.usuario import UsuarioRepositorio

__all__ = [
    "RepositorioBase",
    "TarefaRepositorio",
=======
from app.repositories.usuario import UsuarioRepositorio

__all__ = [
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
    "UsuarioRepositorio",
]