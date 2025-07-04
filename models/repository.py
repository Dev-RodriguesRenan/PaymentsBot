"""
Colunas de pendencias:
    `id`; `Valor da parcela`; `Documento`; `Valor_pendente`; `Emitente`; `C.N.P.J./C.P.F.`; `grupo_centro_de_custo`; `Centro de custo`.
Colunas de baixas:
    `data_baixa`; `id`; `valor`; `documento`; `emitente`; `cnpj_cpf`;`idcentro_custo`; `grupo_centro_custo`; `centro_custo` .
"""

import os
from pprint import pprint
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
    pprint(f"[INFO] DataFrame original:\n{dataframe.head(5)}")
    dataframe = cleaned_dataframe(dataframe)
    pprint(f"[INFO] DataFrame limpo:\n{dataframe.head(5)}")
    columns = columns_mapper(dataframe)
    dataframe = dataframe.rename(columns=columns)
    pprint(f"[INFO] DataFrame renomeado:\n{dataframe.head(5)}")
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
        print(
            f"[ERROR] Não foi possível mover o arquivo {path_file} para a pasta 'data/checked'."
        )

    return dataframe


def payments_df_generator():
    with get_engine().connect() as conn:
        query = """
SELECT 
    pb.id_pendencias_baixas, pb.id, pb.valor_parcela, pb.documento, 
    pb.valor_pendente, 
    pb.emitente, pb.cnpj_cpf, pb.grupo_centro_de_custo, 
    pb.centro_custo, pb.data_baixa, pb.idcentro_custo, 
    pb.filename, pb.created_at, 
    b.id as bordero_id, c.nome as bordero_filename
FROM pendencias_baixas pb JOIN bordero b 
ON pb.cnpj_cpf = b.cnpj_cpf JOIN carga c ON c.id = b.carga_id
"""
        dataframe = pd.read_sql(query, conn)
        dataframe.drop_duplicates(inplace=True)
        return dataframe


def drop_all_payments():
    with get_session() as session:
        payments = session.query(Payments).all()
        for payment in payments:
            session.delete(payment)
        session.commit()
    for file in os.listdir("data/checked"):
        if file.endswith(".xlsx"):
            os.remove(f"data/checked/{file}")
    for file in os.listdir("data/processed"):
        if file.endswith(".xlsx"):
            os.remove(f"data/processed/{file}")
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            os.remove(f"data/{file}")
    pprint("[INFO] All payments and processed files have been dropped.")
