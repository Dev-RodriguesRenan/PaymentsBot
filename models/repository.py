"""
Colunas de pendencias:
    `id`; `Valor da parcela`; `Documento`; `Valor_pendente`; `Emitente`; `C.N.P.J./C.P.F.`; `grupo_centro_de_custo`; `Centro de custo`.
Colunas de baixas:
    `data_baixa`; `id`; `valor`; `documento`; `emitente`; `cnpj_cpf`;`idcentro_custo`; `grupo_centro_custo`; `centro_custo` .
"""

import os
from logger.logger import logger
import shutil
import pandas as pd
from models.conection import get_engine, get_session
from models.entities import Dtype, Payments
from services.payments_service import cleaned_dataframe, columns_mapper


def create_pendencias_baixas(path_file, header):
    dataframe = pd.read_excel(path_file, header=header)
    dataframe = dataframe.dropna(
        how="all", axis=0
    )  # Remove linhas totalmente vazias
    logger.info(f" DataFrame original:\n{dataframe.head(5)}")
    dataframe = cleaned_dataframe(dataframe)
    logger.info(f" DataFrame limpo:\n{dataframe.head(5)}")
    columns = columns_mapper(dataframe)
    dataframe = dataframe.rename(columns=columns)
    logger.info(f" DataFrame renomeado:\n{dataframe.head(5)}")
    # remove linhas onde cnpj_cpf é NaN ou vazio
    dataframe.dropna(subset=["cnpj_cpf"], inplace=True)
    dataframe = dataframe[dataframe["cnpj_cpf"].astype(str).str.strip() != ""]
    dataframe["filename"] = os.path.basename(path_file)
    dataframe["dtype"] = (
        Dtype.PENDENCIAS
        if "pendencias" in os.path.basename(path_file)
        else Dtype.BAIXAS
    )
    with get_engine().connect() as conn:
        dataframe.to_sql(
            Payments.__tablename__,
            con=conn,
            if_exists="append",
            index=False,
        )
    try:
        os.makedirs("data/checked", exist_ok=True)
        shutil.move(path_file, f"data/checked/{os.path.basename(path_file)}")
    except FileNotFoundError:
        logger.critical(
            f"[ERROR] Não foi possível mover o arquivo {path_file} para a pasta 'data/checked'."
        )

    return dataframe


def payments_df_generator():
    with get_engine().connect() as conn:
        query = """
SELECT 
    pb.cnpj_cpf,
    pb.emitente,
    pb.documento,
    pb.valor_parcela, 
    pb.valor_pendente, 
    pb.data_baixa,
    pb.idcentro_custo,
    pb.centro_custo, 
    pb.grupo_centro_de_custo, 
    pb.centro_custo, 
    c.nome as filename, 
    c.origem as base
    # b.id as bordero_id, pb.filename as filename_pagamentos
FROM bordero b JOIN 
carga c on b.carga_id = c.id JOIN
pendencias_baixas pb on b.cnpj_cpf= pb.cnpj_cpf
# AND b.nf = pb.documento -- garante que somente retornem as NFs que estejam no bordero e pendencias baixas
"""
        dataframe = pd.read_sql(query, conn)
        dataframe.drop_duplicates(inplace=True)
        logger.info(f" DataFrame Payments Generated:\n{dataframe.head(5)}")
        return dataframe


def not_occurrence_df_generator():
    with get_engine().connect() as conn:
        query = """
SELECT 
*
FROM bordero b WHERE b.cnpj_cpf not in 
(
	select pb.cnpj_cpf FROM pendencias_baixas pb)
"""
        dataframe = pd.read_sql(query, conn)
        dataframe["cnpj_cpf"].apply(lambda x: str(x).strip())
        dataframe.drop_duplicates(subset=["cnpj_cpf"], inplace=True)
        logger.info(
            f" DataFrame Not Ocurrence Generated:\n{dataframe.head(5)}"
        )
        return dataframe


def drop_all_payments():
    with get_session() as session:
        payments = session.query(Payments).all()
        for payment in payments:
            session.delete(payment)
        session.commit()
    for file in os.listdir("data/checked"):
        if file.endswith(".xlsx"):
            logger.warning(f"removing data/checked/{file}")
            os.remove(f"data/checked/{file}")
    for file in os.listdir("data/processed"):
        if file.endswith(".xlsx"):
            logger.warning(f"removing data/processed/{file}")
            os.remove(f"data/processed/{file}")
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            os.remove(f"data/{file}")
    logger.info(" All payments and processed files have been dropped.")
