import pandas as pd


def converter_para_float(dataframe: pd.DataFrame, coluna: str) -> pd.Series:
    """
    Converte os valores textuais de uma coluna para float.

    A função remove separadores de milhar, substitui a vírgula decimal por ponto
    e converte os valores resultantes para o tipo float.

    Args:
        dataframe: DataFrame que contém a coluna a ser convertida.
        coluna: Nome da coluna com os valores textuais numéricos.

    Returns:
        Series contendo os valores convertidos para float.
    """

    return (
        dataframe[coluna]
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )


def converter_para_datetime(dataframe: pd.DataFrame, coluna: str) -> pd.Series:
    """
    Converte os valores de uma coluna para datetime.

    A conversão utiliza o formato ``%d/%m/%Y`` e valores inválidos são
    transformados em ``NaT``.

    Args:
        dataframe: DataFrame que contém a coluna a ser convertida.
        coluna: Nome da coluna com os valores de data.

    Returns:
        Series contendo os valores convertidos para datetime.
    """

    return pd.to_datetime(
        dataframe[coluna],
        format="%d/%m/%Y",
        errors="coerce",
        dayfirst=True
    )


if __name__ == "__main__":

    dados = {
        "id": [1, 2, 3, 4, 5],
        "nome": ["Ana", "Bruno", "Carlos", "Diana", "Eduardo"],
        "idade": [23, 30, 19, 27, 35],
        "cidade": ["Fortaleza", "São Paulo", "Rio", "BH", "Curitiba"],
        "nota": ["8.053,5", "31.327,50", "9,2", "6,8", "8,0"],
    }

    df = pd.DataFrame(dados)
    df['nota'] = converter_para_float(df, 'nota')

    print(df.dtypes)
    print(df)
