import pandas as pd
from pprint import pprint


def cleaned_dataframe(dataframe: pd.DataFrame):
    # Define as colunas permitidas (normalizadas para facilitar a comparação)
    allowed_columns = [
        "id",
        "valor da parcela",
        "documento",
        "valor pendente",
        "emitente",
        "cnpj/cpf",
        "grupo centro de custo",
        "centro de custo",
        "data baixa",
        "valor",
        "cnpj cpf",
        "idcentro custo",
        "grupo centro custo",
        "centro custo",
    ]
    for column in dataframe.columns:
        if (
            column.lower().replace(".", "").replace("_", " ")
            not in allowed_columns
        ):
            pprint(f"Coluna '{column}' não permitida. Removendo do DataFrame.")
            dataframe.drop(columns=[column], inplace=True)

    return dataframe


def columns_mapper(dataframe: pd.DataFrame):
    columns = {}
    for column in dataframe.columns:
        # remove ., espaços antes e depois, substitui _ por espaço e transforma em minúsculas
        column_cleaned = (
            column.strip()
            .lower()
            .replace(".", "")
            .replace(" ", "_")
            .replace("_", " ")
        )
        if column_cleaned == "id":
            columns[column] = "id"
        elif column_cleaned in ["valor da parcela", "valor"]:
            columns[column] = "valor_parcela"
        elif column_cleaned == "documento":
            columns[column] = "documento"
        elif column_cleaned == "valor pendente":
            columns[column] = "valor_pendente"
        elif column_cleaned == "emitente":
            columns[column] = "emitente"
        elif column_cleaned in ["cnpj/cpf", "cnpj_cpf"]:
            columns[column] = "cnpj_cpf"
        elif column_cleaned in ["grupo centro de custo", "grupo centro custo"]:
            columns[column] = "grupo_centro_de_custo"
        elif column_cleaned == "centro de custo":
            columns[column] = "centro_custo"
    pprint(f"[INFO] Colunas mapeadas: {columns}")
    return columns
