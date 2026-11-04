"""Testes das regras básicas do usuário."""
import pytest

from app.core.exceptions import ValorInvalido
from app.core.security import HashDeSenha
from app.models.usuario import Usuario


class HashFake(HashDeSenha):
    def gerar(self, senha: str) -> str:
        return f"fake:{senha}"

    def verificar(self, senha: str, hash_armazenado: str) -> bool:
        return hash_armazenado == f"fake:{senha}"


def test_usuario_normaliza_email():
    usuario = Usuario(nome="Debora", email="  TESTE@EXEMPLO.COM ")
    assert usuario.email == "teste@exemplo.com"


def test_nome_vazio_e_rejeitado():
    with pytest.raises(ValorInvalido):
        Usuario(nome="   ", email="teste@exemplo.com")


def test_usuario_protege_e_confere_senha():
    usuario = Usuario(nome="Debora", email="teste@exemplo.com")
    hasher = HashFake()
    usuario.definir_senha("senha123", hasher)

    assert usuario._senha_hash != "senha123"
    assert usuario.senha_confere("senha123", hasher)
    assert not usuario.senha_confere("outra", hasher)