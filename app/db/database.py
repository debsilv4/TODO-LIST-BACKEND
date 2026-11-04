"""Configuração da conexão e das sessões do banco de dados."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import obter_configuracao


def _opcoes_do_engine(url: str) -> dict:
    """Define as opções de conexão conforme o banco utilizado."""
    if url.startswith("sqlite"):
        opcoes = {
            "connect_args": {"check_same_thread": False}
        }

        if url in (
            "sqlite://",
            "sqlite:///:memory:",
            "sqlite+pysqlite:///:memory:",
        ):
            opcoes["poolclass"] = StaticPool

        return opcoes

    return {"pool_pre_ping": True}


_url = obter_configuracao().url_banco

engine: Engine = create_engine(
    _url,
    echo=False,
    **_opcoes_do_engine(_url),
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def criar_tabelas() -> None:
    """Cria as tabelas definidas nos modelos."""
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def obter_sessao() -> Generator[Session, None, None]:
    """Disponibiliza uma sessão do banco para cada requisição."""
    sessao = SessionLocal()

    try:
        yield sessao
    finally:
        sessao.close()