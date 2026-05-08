from typing import cast

from openpyxl.worksheet.worksheet import Worksheet

from config import (
    CAIXA_PROCESSADO,
    DESTINO_HISTORICO,
    DESTINO_VALOR,
    PROCESSED_FILE,
    RAW_FILE,
    TEMPLATE_CAIXA,
)
from escritor_caixa import carregar_modelo_caixa, preencher_planilha
from leitor_bradesco import ler_extrato_bradesco
from processamento_pix import extrair_pix, salvar_extrato_processado


def main() -> None:
    # Leitura do extrato do bradesco
    extrato = ler_extrato_bradesco(RAW_FILE)

    # Extração dos pix corretos e formatação dos valores
    extrato = extrair_pix(extrato)

    # Salvar o extrato formatado
    salvar_extrato_processado(extrato, PROCESSED_FILE)

    # Carregar o modelo do caixa
    wb = carregar_modelo_caixa(TEMPLATE_CAIXA)
    ws = cast(Worksheet, wb.active)

    # Escrever os dados filtrados na planilha modelo
    ws = preencher_planilha(ws, extrato, DESTINO_HISTORICO, DESTINO_VALOR)

    # Salvar caixa preenchindo com os pix
    wb.save(CAIXA_PROCESSADO)


if __name__ == "__main__":
    main()
