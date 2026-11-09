"""Serviços de aplicação: onde as operações do sistema são orquestradas.

Um serviço recebe repositórios e colaboradores pelo construtor (injeção de
dependência), aplica as regras de negócio e levanta exceções de domínio. Ele
não conhece HTTP: não importa `fastapi`, não devolve códigos de status. O
mesmo serviço funcionaria em um programa de terminal.
"""

<<<<<<< HEAD
from app.services.tarefa import TarefaServico
=======
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
from app.services.usuario import Sessao, UsuarioServico

__all__ = [
    "Sessao",
<<<<<<< HEAD
    "TarefaServico"
=======
>>>>>>> 597d2eec1812248764924f270aa3d343d1591fbe
    "UsuarioServico",
]
