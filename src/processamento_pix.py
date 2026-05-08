from datetime import datetime
from pathlib import Path

import pandas as pd

from config import FLAG_PIX, PREFIXO_PIX, PROCESSED_FILE, RAW_FILE
from leitor_bradesco import ler_extrato_bradesco


def formatar_pix(dataframe: pd.DataFrame, coluna: str) -> pd.Series:
    """
    Formata os registros de PIX de uma coluna do DataFrame.

    A função remove o prefixo definido em ``PREFIXO_PIX``, elimina a data ao final
    da string quando presente, remove espaços extras e padroniza o texto no
    formato título.

    Args:
        dataframe: DataFrame contendo os dados a serem formatados.
        coluna: Nome da coluna que contém os lançamentos de PIX.

    Returns:
        Series com os lançamentos formatados.
    """

    # Cópia segura do dataframe original
    df: pd.DataFrame = dataframe.copy()

    extrato_pix = df

    # Remoção de um prefixo desnecessário para visualização  do pix
    # e padronização da string
    extrato_pix[coluna] = (
        extrato_pix[coluna]
        .str.replace(fr"\b{PREFIXO_PIX}\b", "Pix - ", regex=True)
        .str.replace(r"\s+\d{2}/\d{2}$", "", regex=True)
        .str.strip()
        .str.title()
    )

    return extrato_pix["lancamento"]


def extrair_pix(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Extrai e filtra os lançamentos de PIX do dia atual.

    A função seleciona apenas registros cujo lançamento começa com o prefixo
    definido em ``PREFIXO_PIX``, formata esses lançamentos, filtra os registros
    para a data de hoje e remove os PIX associados a outras lojas com base em
    ``FLAG_PIX``.

    Args:
        dataframe: DataFrame contendo os lançamentos do extrato bancário.

    Returns:
        DataFrame contendo apenas os registros de PIX válidos do dia atual.
    """

    # Filtragem dos pix e cópia segura do dataframe original
    extrato_pix: pd.DataFrame = dataframe.loc[
        dataframe["lancamento"].str.startswith(PREFIXO_PIX, na=False)
    ].copy()

    # Formatação dos pix
    extrato_pix['lancamento'] = formatar_pix(extrato_pix, "lancamento")

    # coletando data de hoje
    hoje = datetime.today().date()

    # filtragem para pegar os pix só de hoje
    filtro_data = (extrato_pix['data'].dt.date == hoje)
    extrato_pix = extrato_pix.loc[filtro_data].copy()

    # Filtragem pra remover os pix que são de outra loja
    filtro_pix_outra_loja = (~extrato_pix['lancamento'].isin(FLAG_PIX))
    extrato_pix = extrato_pix.loc[filtro_pix_outra_loja].copy()

    return extrato_pix


def salvar_extrato_processado(dataframe: pd.DataFrame, path: Path) -> None:
    """
    Salva o DataFrame processado em um arquivo CSV.

    A função garante que o diretório de destino exista antes de salvar o
    arquivo utilizando separador por ponto e vírgula e codificação UTF-8 com BOM.

    Args:
        dataframe: DataFrame que será salvo.
        path: Caminho completo do arquivo de saída.

    Returns:
        None.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(
        path,
        sep=";",
        index=False,
        encoding="utf-8-sig"
    )


if __name__ == "__main__":
    extrato = ler_extrato_bradesco(RAW_FILE)
    extrato = extrair_pix(extrato)
    salvar_extrato_processado(extrato, PROCESSED_FILE)

    print(datetime.today().date())
    print(extrato['data'].head(5))
