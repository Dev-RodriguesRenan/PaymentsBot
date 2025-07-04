"""
Colunas de pendencias:
    `id`; `Valor da parcela`; `Documento`; `Valor_pendente`; `Emitente`; `C.N.P.J./C.P.F.`; `grupo_centro_de_custo`; `Centro de custo`.
Colunas de baixas:
    `data_baixa`; `id`; `valor`; `documento`; `emitente`; `cnpj_cpf`;`idcentro_custo`; `grupo_centro_custo`; `centro_custo` .
"""

import os
from pprint import pprint
import pandas as pd
from models.conection import get_engine
from models.entities import PendenciasBaixas


def create_pendencias_baixas(path_file, header):
    dataframe = pd.read_excel(path_file, header=header)
    dataframe = dataframe.dropna(
        how="all", axis=0
    )  # Remove linhas totalmente vazias
    pprint(f"[INFO] DataFrame original:\n{dataframe.head(5)}")
    dataframe = cleaned_dataframe(dataframe)
    pprint(f"[INFO] DataFrame limpo:\n{dataframe.head(5)}")
    columns = columns_mapper(dataframe)
    dataframe = dataframe.rename(columns=columns)
    pprint(f"[INFO] DataFrame renomeado:\n{dataframe.head(5)}")
    dataframe["filename"] = os.path.basename(path_file)
    with get_engine().connect() as conn:
        dataframe.to_sql(
            PendenciasBaixas.__tablename__,
            con=conn,
            if_exists="append",
            index=False,
        )
    return dataframe


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
            print(f"Coluna '{column}' não permitida. Removendo do DataFrame.")
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
