import datetime
import os
from models.base import Base
from models.conection import get_engine
from models.db_actions import create_pendencias_baixas, payments_df_generator

Base.metadata.create_all(get_engine())


def main():
    print("Database and tables created successfully.")
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            print(f"[INFO] Processing file: {file}")
            header = 4 if "RealizacoesBaixas" in file else 3
            create_pendencias_baixas(f"data/{file}", header)
            print(f"[INFO] File {file} processed successfully.")
    dataframe = payments_df_generator()
    dataframe.to_excel(
        f"data/processed/RelatorioDePagamentos_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        index=False,
    )
    print(f"[INFO] DataFrame genereted.", dataframe.head())


if __name__ == "__main__":
    dataframe = payments_df_generator()
    dataframe.to_excel(
        f"data/processed/RelatorioDePagamentos_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        index=False,
    )
    print(f"[INFO] DataFrame genereted.", dataframe.head())
