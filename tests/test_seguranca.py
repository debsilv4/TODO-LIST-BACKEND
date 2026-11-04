"""Testes da proteção de senhas."""
from app.core.security import HashBcrypt, LIMITE_BYTES_SENHA


def test_bcrypt_gera_hash_e_verifica_senha():
    hasher = HashBcrypt()
    hash_senha = hasher.gerar("senha-segura-123")

    assert hash_senha != "senha-segura-123"
    assert hasher.verificar("senha-segura-123", hash_senha)
    assert not hasher.verificar("senha-errada", hash_senha)


def test_bcrypt_recusa_senha_acima_do_limite():
    hasher = HashBcrypt()
    senha_longa = "a" * (LIMITE_BYTES_SENHA + 1)

    assert not hasher.verificar(senha_longa, "hash-invalido")