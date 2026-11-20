"""Criptografando um arquivo com senha sem excluir o original por segurança"""
import argparse
import getpass
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"ENC1"


def derivar_chave(senha: str, salt: bytes) -> bytes:
    return Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(senha.encode("utf-8"))


def criptografar(origem: Path, senha: str) -> Path:
    if not origem.is_file():
        raise ValueError("Informe um arquivo existente.")
    destino = origem.with_name(origem.name + ".enc")
    salt, nonce = os.urandom(16), os.urandom(12)
    dados = origem.read_bytes()
    cabecalho = MAGIC + salt + nonce
    cifrado = AESGCM(derivar_chave(senha, salt)).encrypt(nonce, dados, cabecalho)
    with destino.open("xb") as arquivo:
        arquivo.write(cabecalho + cifrado)
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description="Criptografa um arquivo sem apagar o original")
    parser.add_argument("arquivo", type=Path)
    args = parser.parse_args()
    senha = getpass.getpass("Senha: ")
    if not senha:
        parser.error("A senha não pode estar vazia")
    try:
        destino = criptografar(args.arquivo, senha)
        print(f"Arquivo criptografado: {destino}")
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
