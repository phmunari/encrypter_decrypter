"""Descriptografando arquivo .enc criados pelo encrypter_melhorado.py."""
import argparse
import getpass
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"ENC1"


def derivar_chave(senha: str, salt: bytes) -> bytes:
    return Scrypt(salt=salt, length=32, n=2**14, r=8, p=1).derive(senha.encode("utf-8"))


def descriptografar(origem: Path, senha: str) -> Path:
    if not origem.is_file() or origem.suffix != ".enc":
        raise ValueError("Informe um arquivo .enc existente.")
    conteudo = origem.read_bytes()
    if len(conteudo) < 48 or conteudo[:4] != MAGIC:
        raise ValueError("Formato de arquivo inválido.")
    cabecalho, cifrado = conteudo[:32], conteudo[32:]
    salt, nonce = cabecalho[4:20], cabecalho[20:32]
    dados = AESGCM(derivar_chave(senha, salt)).decrypt(nonce, cifrado, cabecalho)
    destino = origem.with_suffix("")
    with destino.open("xb") as arquivo:
        arquivo.write(dados)
    return destino


def main() -> None:
    parser = argparse.ArgumentParser(description="Descriptografa um arquivo .enc sem apagar o original")
    parser.add_argument("arquivo", type=Path)
    args = parser.parse_args()
    senha = getpass.getpass("Senha: ")
    try:
        destino = descriptografar(args.arquivo, senha)
        print(f"Arquivo recuperado: {destino}")
    except InvalidTag:
        parser.exit(1, "Erro: senha incorreta ou arquivo alterado.\n")
    except (OSError, ValueError) as erro:
        parser.exit(1, f"Erro: {erro}\n")


if __name__ == "__main__":
    main()
