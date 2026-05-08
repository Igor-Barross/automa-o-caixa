from pathlib import Path
from typing import cast

import openpyxl as op
import pandas as pd

# from openpyxl.cell.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from config import (
    CAIXA_PROCESSADO,
    CELULA_SOMA_PIX,
    DATA_DIA_ATUAL,
    DESTINO_HISTORICO,
    DESTINO_VALOR,
    PROCESSED_FILE,
    TEMPLATE_CAIXA,
)


def carregar_modelo_caixa(path: Path) -> op.Workbook:
    """
    Carrega e retorna a planilha modelo do caixa a partir de um caminho informado.

    Args:
        path: Caminho do arquivo Excel que será carregado.

    Returns:
        Workbook carregado com o conteúdo do arquivo informado.
    """
    wb = op.load_workbook(path)

    return wb


def preencher_planilha(
        planilha: Worksheet,
        dataframe: pd.DataFrame,
        destino_historico: list,
        destino_valor: list) -> Worksheet:
    """
    Preenche a planilha com os lançamentos e valores do DataFrame.

    Os textos da coluna ``lancamento`` são distribuídos nas células definidas em
    ``destino_historico``. Os valores da coluna ``credito`` são inseridos nas
    células definidas em ``destino_valor``. Ao final, a função escreve a fórmula
    de soma dos valores de PIX em ``CELULA_SOMA_PIX`` e atualiza a célula
    ``E2`` com a data atual.

    Args:
        planilha: Planilha do Excel que será preenchida.
        dataframe: DataFrame com os dados que serão inseridos na planilha.
        destino_historico: Lista com os intervalos de destino para os lançamentos.
        destino_valor: Lista com os intervalos de destino para os valores.

    Returns:
        A planilha preenchida com os dados, a fórmula de soma e a data.
    """

    # essas são as celulas que utilizirei para criar a função que some os pix
    # existe um celula na planiha modelo, que é dedicada para essa função
    primeira_celula: str | None = None
    ultima_celula: str | None = None

    df = dataframe.copy()
    indice = 0

    for destino in destino_historico:
        coluna: str = destino["coluna"]
        min_row: int = destino["min_row"]
        max_row: int = destino["max_row"]

        for row in range(min_row, max_row + 1):
            if indice >= len(df):
                break

            celula: str = f"{coluna}{row}"
            planilha[celula] = df['lancamento'].iloc[indice]

            indice += 1

    indice = 0

    for destino in destino_valor:
        coluna: str = destino["coluna"]
        min_row: int = destino["min_row"]
        max_row: int = destino["max_row"]

        for row in range(min_row, max_row + 1):
            if indice >= len(df):
                break

            celula: str = f"{coluna}{row}"

            if primeira_celula is None:
                primeira_celula = celula

            ultima_celula = celula

            planilha[celula] = df['credito'].iloc[indice]
            indice += 1

    planilha[CELULA_SOMA_PIX] = f"=SUM({primeira_celula}:{ultima_celula})"

    planilha['E2'] = f"DATA: {DATA_DIA_ATUAL}"

    return planilha


if __name__ == "__main__":
    wb: op.Workbook = carregar_modelo_caixa(TEMPLATE_CAIXA)
    ws = cast(Worksheet, wb.active)

    df = pd.read_csv(PROCESSED_FILE, sep=";",)

    ws = preencher_planilha(ws, df, DESTINO_HISTORICO, DESTINO_VALOR)

    wb.save(CAIXA_PROCESSADO)
