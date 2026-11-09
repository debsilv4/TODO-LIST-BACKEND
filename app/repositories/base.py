"""Contrato base para repositórios."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy.orm import Session


T = TypeVar("T")


class RepositorioBase(ABC, Generic[T]):
    """Define operações básicas de persistência."""

    def __init__(self, sessao: Session) -> None:
        self.sessao = sessao

    @property
    @abstractmethod
    def modelo(self) -> type[T]:
        """Modelo associado ao repositório."""
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, identificador: int) -> T | None:
        """Busca um registro pelo identificador."""
        raise NotImplementedError

    def salvar(self, entidade: T) -> T:
        """Salva uma entidade no banco de dados."""
        self.sessao.add(entidade)
        self.sessao.commit()
        self.sessao.refresh(entidade)
        return entidade

    def remover(self, entidade: T) -> None:
        """Remove uma entidade do banco."""
        self.sessao.delete(entidade)
        self.sessao.commit()