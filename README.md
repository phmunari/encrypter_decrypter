# File Encryption Tool — Python AES-256-GCM

Ferramenta educacional de linha de comando para **criptografar e descriptografar arquivos locais** com Python. O projeto utiliza **AES-256-GCM** para proteger a confidencialidade e verificar a integridade dos dados, preservando os arquivos originais.

> **Uso recomendado:** estudos de Python e criptografia, com arquivos próprios e cópias de teste. Esta ferramenta não substitui soluções auditadas de proteção de dados ou backup, nem deve ser usada com o objetivo de prejudicar outras pessoas.

> Um projeto baseado no desafio de criação de Ramsomware do bootcamp de Cibersegurnaça da DIO. 
    O projeto original se encontra em https://github.com/cassiano-dio/cibersecurity-desafio-ransomware/tree/master
    
## Funcionalidades

- Criptografia e descriptografia por meio de dois scripts independentes.
- AES-256-GCM, com autenticação dos dados criptografados.
- Derivação de chave a partir de senha usando **Scrypt**.
- *Salt* aleatório de 16 bytes e *nonce* aleatório de 12 bytes por criptografia.
- Solicitação de senha no terminal, sem exibi-la na tela.
- Preservação do arquivo de origem; não apaga nem sobrescreve arquivos existentes.
- Mensagens de erro para caminhos inválidos, formato incompatível e falha de autenticação.

## Estrutura do projeto

```text
projeto/
├── encrypt.py
├── decrypt.py
└── README.md
```

## Requisitos

- Python 3.9 ou superior (recomendado).
- Biblioteca Python `cryptography`.

### Instalação no Fedora/Linux

Na pasta do projeto, crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install cryptography
```

Caso o módulo `venv` não esteja disponível, instale o suporte correspondente à sua distribuição.

## Como usar

### 1. Criptografar um arquivo

Crie um arquivo de teste:

```bash
echo "Mensagem de teste" > teste.txt
```

Execute:

```bash
python3 encrypt.py teste.txt
```

Digite uma senha quando solicitado. O programa criará `teste.txt.enc` na mesma pasta, **sem excluir `teste.txt`**.

### 2. Descriptografar um arquivo

O programa não sobrescreve um arquivo existente. Como `teste.txt` ainda está na pasta, mova o arquivo criptografado para um diretório separado antes de testar a recuperação:

```bash
mkdir -p recuperados
mv teste.txt.enc recuperados/
python3 decrypt.py recuperados/teste.txt.enc
```

Informe **a mesma senha** usada na criptografia. O resultado será `recuperados/teste.txt`.

### 3. Verificar o resultado

Compare os hashes SHA-256 do arquivo original e do recuperado:

```bash
sha256sum teste.txt recuperados/teste.txt
```

Os dois hashes devem ser idênticos.

## Como funciona

1. O usuário informa um arquivo e uma senha.
2. O script gera um *salt* aleatório e deriva uma chave de 32 bytes usando Scrypt (`n=2^14`, `r=8`, `p=1`).
3. Um *nonce* aleatório de 12 bytes é gerado para o AES-GCM.
4. O conteúdo é criptografado e autenticado, incluindo o cabeçalho como dado adicional autenticado (AAD).
5. O arquivo `.enc` recebe o cabeçalho e os dados criptografados com a tag de autenticação.
6. Na descriptografia, o programa recupera o *salt* e o *nonce*, deriva novamente a chave e verifica a autenticação antes de salvar os dados.

### Formato do arquivo `.enc`

| Campo | Tamanho | Descrição |
|---|---:|---|
| Identificador `ENC1` | 4 bytes | Identifica o formato |
| Salt | 16 bytes | Usado pelo Scrypt |
| Nonce | 12 bytes | Usado pelo AES-GCM |
| Conteúdo criptografado | Variável | Dados protegidos |
| Tag GCM | 16 bytes | Autenticação e integridade |

O cabeçalho tem **32 bytes** e é autenticado como AAD. O identificador `ENC1` é um formato próprio deste projeto, não um padrão universal.

## Segurança e limitações

- **Não perca a senha:** o projeto não possui mecanismo de recuperação.
- Use uma senha longa, única e difícil de adivinhar.
- Os scripts não excluem os arquivos originais nem sobrescrevem arquivos de saída existentes.
- Uma senha incorreta ou alterações no arquivo criptografado causam falha de autenticação.
- O conteúdo é carregado integralmente na memória; arquivos grandes podem consumir muita RAM.
- O nome do arquivo e alguns metadados do sistema de arquivos **não são criptografados**.
- Os arquivos `.enc` não são compatíveis com os antigos `.ransomwaretroll` produzidos pelos scripts com `pyaes` e AES-CTR.
- Para dados sensíveis ou produção, prefira ferramentas consolidadas e auditadas, além de manter backups independentes.

## Melhorias futuras

- [ ] Processamento em blocos para arquivos grandes.
- [ ] Testes automatizados com `pytest`.
- [ ] Opção de escolher o diretório de saída.
- [ ] Empacotamento como ferramenta de linha de comando.
- [ ] Documentação de testes de segurança e compatibilidade.

## Tecnologias

- Python 3
- [`cryptography`](https://cryptography.io/)
- AES-256-GCM
- Scrypt
- `argparse`, `getpass` e `pathlib`

## Objetivo

Projeto desenvolvido para praticar **programação Python, manipulação de arquivos, tratamento de exceções e fundamentos de criptografia aplicada**, sendo desenvolvido para um projeto de cibersegurança.
