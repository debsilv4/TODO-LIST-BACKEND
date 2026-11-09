"""Fixtures de teste usando um banco SQLite temporário."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, obter_sessao
from app.main import app
import app.models  # noqa: F401


@pytest.fixture()
def banco_teste():
    engine_teste = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SessaoTeste = sessionmaker(
        bind=engine_teste,
        autoflush=False,
        autocommit=False,
    )
    Base.metadata.create_all(bind=engine_teste)
    yield SessaoTeste
    Base.metadata.drop_all(bind=engine_teste)
    engine_teste.dispose()


@pytest.fixture()
def cliente(banco_teste):
    def override_obter_sessao():
        sessao = banco_teste()
        try:
            yield sessao
        finally:
            sessao.close()

    app.dependency_overrides[obter_sessao] = override_obter_sessao
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()