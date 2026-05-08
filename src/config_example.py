from datetime import datetime
from pathlib import Path

"""
Arquivo de exemplo de configuração do projeto.

OBJETIVO
--------
Este arquivo existe para servir como modelo público do seu `config.py`.
A ideia é que quem clonar o projeto copie este arquivo, renomeie para
`config.py` e então preencha os valores necessários conforme a estrutura
local da máquina e os dados do próprio projeto.

COMO USAR
---------
1. Copie este arquivo.
2. Renomeie a cópia para `config.py`.
3. Revise cada constante marcada como configurável.
4. Ajuste nomes de arquivos, caminhos, prefixos e flags conforme sua realidade.

EXEMPLO
-------
No terminal:

    cp config_example.py config.py

Depois disso, altere o `config.py` e mantenha este arquivo como referência
para o repositório.

OBSERVAÇÕES IMPORTANTES
-----------------------
- Evite colocar dados sensíveis aqui.
- Se a estrutura de pastas do projeto mudar, atualize este arquivo também.
- Sempre que adicionar uma nova configuração no `config.py` real,
  replique aqui com uma explicação simples.
"""


# ------ CAMINHOS PASTAS PRINCIPAIS ------
# Esses caminhos assumem que este arquivo está dentro de uma pasta do projeto
# e que a raiz dele fica um nível acima, conforme a estrutura atual.
# Se sua estrutura mudar, revise principalmente o BASE_DIR.

BASE_DIR = Path(__file__).parents[1]
DATA_DIR = BASE_DIR / "data"
NOTEBOOK_DIR = BASE_DIR / "notebooks"
REFERENCES_DIR = BASE_DIR / "references"
SRC_DIR = BASE_DIR / "src"
TESTS_DIR = BASE_DIR / "tests"
TEMPLATE_DIR = BASE_DIR / "templates"
OUTPUT_DIR = BASE_DIR / "output"


# ------ CAMINHOS DAS SUBPASTAS ------
# Ajuste aqui caso você mude o nome das subpastas dentro de data/.

RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"


# ------ CAMINHO DO EXTRATO ------
# Informe os arquivos de entrada e saída usados no processamento.
# RAW_FILE: arquivo bruto original.
# PROCESSED_FILE: arquivo gerado após limpeza/tratamento.
# Se seu extrato vier com outro nome, altere apenas o nome do arquivo.

RAW_FILE = RAW_DATA / "extrato.csv"
PROCESSED_FILE = PROCESSED_DATA / "extrato_processado.csv"


# ------ CAMINHO TEMPLATE DO CAIXA ------
# Arquivo modelo da planilha que será preenchida pelo script.
# Troque esse nome caso o template da sua empresa/loja tenha outro nome.

TEMPLATE_CAIXA = TEMPLATE_DIR / "modelo_caixa.xlsx"


# ------ DATA DO DIA ATUAL ------
_data_hoje = datetime.now()
DATA_DIA_ATUAL = _data_hoje.strftime('%d-%m-%Y')


# ------ CAMINHO CAIXA FINALIZADO ------
# Gera automaticamente o nome da planilha final com a data atual.
# Exemplo de saída: Caixa Horizonte 07-05-2026.xlsx
# Se quiser mudar o padrão do nome, edite a f-string abaixo.
CAIXA_PROCESSADO = OUTPUT_DIR / f'Caixa {DATA_DIA_ATUAL}.xlsx'


# ------ PREFIXO PARA FILTRAR PIX ------
# Prefixo usado para identificar lançamentos PIX no histórico do extrato.
# Preencha exatamente como o texto aparece no banco.
# Exemplo: "TRANSFERENCIA PIX REM: "
# Se o extrato mudar de padrão, este é um dos primeiros pontos que você deve revisar.

PREFIXO_PIX = "TRANSFERENCIA PIX REM: "


# ------ NOMES DE PIX DE OUTRA LOJA ------
# Lista de descrições que devem ser tratadas como exceção, ignoradas
# ou sinalizadas separadamente (dependendo da lógica do seu projeto).
# Mantenha cada item como string.
# Adicione novos nomes conforme forem aparecendo no extrato.
# Adicione da maneira como já estivesse formatado e não como vem do extrato.


FLAG_PIX = [
    "Pix - NOME",
]


# ------ AREA PRA SER PREENCHIDA NO MODELO CAIXA ------
# Essa área define onde os dados serão inseridos na planilha modelo.
# Cada dicionário informa:
# - coluna: coluna da planilha Excel
# - min_row: linha inicial
# - max_row: linha final
#
# DESTINO_HISTORICO:
# Onde os nomes/históricos dos PIX serão escritos.
#
# DESTINO_VALOR:
# Onde os valores correspondentes serão escritos.
#
# IMPORTANTE:
# O ideal é que a quantidade de linhas em DESTINO_HISTORICO e DESTINO_VALOR
# esteja alinhada com o layout do seu template.
# Se a planilha mudar, confira essas posições manualmente no Excel.

DESTINO_HISTORICO = [
    {'coluna': 'A', 'min_row': 11, 'max_row': 27},
    {'coluna': 'C', 'min_row': 11, 'max_row': 27},
]

DESTINO_VALOR = [
    {'coluna': 'B', 'min_row': 11, 'max_row': 27},
    {'coluna': 'D', 'min_row': 11, 'max_row': 27},
]


# ------ CONFIGURAÇÕES DA PLANILHA MODELO ------
# Célula usada para armazenar ou conferir a soma total dos PIX.
# Confirme no template se essa referência continua correta.
# Exemplo: se a soma mudar de G15 para H20, atualize aqui.

CELULA_SOMA_PIX = 'G15'
