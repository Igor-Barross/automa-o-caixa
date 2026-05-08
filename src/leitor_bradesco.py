from pathlib import Path

import pandas as pd

from config import RAW_FILE
from utils import converter_para_datetime, converter_para_float


def ler_extrato_bradesco(path: Path) -> pd.DataFrame:
    extrato: pd.DataFrame = pd.read_csv(
        path,
        sep=";",
        skiprows=1,
        encoding="latin1"
    )
    """
    Lê o extrato do Bradesco a partir de um arquivo CSV e retorna um DataFrame tratado.

    A função carrega o arquivo, remove colunas desnecessárias, padroniza os nomes
    das colunas, converte a coluna de data para datetime e transforma a coluna de
    crédito em valores numéricos.

    Args:
        path: Caminho do arquivo CSV do extrato bancário.

    Returns:
        DataFrame contendo as colunas tratadas de data, lançamento e crédito.
    """

    # Removendo colunas desnecessárias para nosso objetivo
    extrato = extrato.drop(columns=['Dcto.', 'Débito (R$)'])

    # Padronização dos nomes das colunas
    extrato.columns = ['data', 'lancamento', 'credito']

    # Convertendo o tipo da coluna 'data' para datetime
    extrato['data'] = converter_para_datetime(extrato, 'data')

    # Removendo uma string na coluna de 'credito',
    extrato['credito'] = extrato['credito'].str.replace('Crédito (R$)', '0')

    # Converterndo o tipo da coluna 'credito' para float
    extrato['credito'] = converter_para_float(extrato, 'credito')

    return extrato


if __name__ == "__main__":
    extrato = ler_extrato_bradesco(RAW_FILE)
    print(extrato)
