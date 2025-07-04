import datetime
import os
import subprocess
from models.base import Base
from models.conection import get_engine
from models.repository import create_pendencias_baixas, payments_df_generator
from pprint import pprint

Base.metadata.create_all(get_engine())


def run_file(path_file):
    try:
        pprint("[INFO] Starting robot...")
        if not os.path.exists(path_file):
            raise FileNotFoundError(f"[ERROR] File {path_file} not found.")
        subprocess.run(["python", "-m", "robot", "-d", "results", path_file])
        pprint("[INFO] Robot finished successfully.")
    except Exception as e:
        pprint(f"[ERROR] An error occurred while running the robot: {e}")
        raise

def main():
    for folder in os.listdir("suites"):
        for file in os.listdir(f"suites/{folder}"):
            if file.endswith(".robot"):
                run_file(f"suites/{folder}/{file}")
    pprint("Database and tables created successfully.")
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            pprint(f"[INFO] Processing file: {file}")
            header = 4 if "RealizacoesBaixas" in file else 3
            create_pendencias_baixas(f"data/{file}", header)
            pprint(f"[INFO] File {file} processed successfully.")
    dataframe = payments_df_generator()
    if dataframe.empty:
        pprint("[WARNING] No data found in the database.")
        return
    dataframe.to_excel(
        f"data/processed/RelatorioDePagamentos_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        index=False,
    )
    pprint("[INFO] DataFrame genereted.", dataframe.head())


if __name__ == "__main__":
    main()
