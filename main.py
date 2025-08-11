import datetime
import os
import subprocess
import sys
import time
from models.base import Base
from models.conection import get_engine
from models.repository import (
    create_pendencias_baixas,
    drop_all_payments,
    not_occurrence_df_generator,
    payments_df_generator,
)
from logger.logger import logger
import schedule

from whatsapp.whatsapp import send_whatsapp

Base.metadata.create_all(get_engine())
contatos = os.getenv("CONTATOS").split(",")


def run_file(path_file):
    try:
        logger.info(" Starting robot...")
        if not os.path.exists(path_file):
            raise FileNotFoundError(f"[ERROR] File {path_file} not found.")
        subprocess.run(
            [
                "venv/Scripts/python.exe",
                "-m",
                "robot",
                "-d",
                "results",
                path_file,
            ]
        )
        logger.info(" Robot finished successfully.")
    except Exception as e:
        logger.critical(
            f"[ERROR] An error occurred while running the robot: {e}"
        )
        raise


def main():
    # check if the current day is a weekend (Saturday or Sunday)
    if datetime.datetime.now().weekday() in [5, 6]:
        logger.info(" Today is not a weekend, skipping execution.")
        return
    # clear database payments table before running the scripts
    drop_all_payments()
    # execute all robot files in the suites directory
    for folder in os.listdir("suites"):
        for file in os.listdir(f"suites/{folder}"):
            if file.endswith(".robot"):
                run_file(f"suites/{folder}/{file}")
    logger.info("Database and tables created successfully.")
    # check if the data directory exists and create pendencias baixas
    if len(os.listdir('data')) < 2: raise FileNotFoundError('O diretorio não contem ambos os relatorios, verifique e tente novamente')
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            logger.info(f" Processing file: {file}")
            header = 4 if "RealizacoesBaixas" in file else 3
            create_pendencias_baixas(f"data/{file}", header)
            logger.info(f" File {file} processed successfully.")
    # generate payments dataframe, export in excel file and send by whatsApp
    dataframe = payments_df_generator()
    df_no_occurrencies = not_occurrence_df_generator()
    if dataframe.empty:
        logger.warning("[WARNING] No data found in the database.")
        return
    filename_rel_payments = f"data/processed/RelatorioDePagamentos_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    dataframe.to_excel(
        filename_rel_payments,
        index=False,
    )
    filename_not_ocurrencies = None
    if not df_no_occurrencies.empty:
        filename_not_ocurrencies = (
            "data/not_occurencies/RelatorioDeNaoOcorrencias.xlsx"
        )
        df_no_occurrencies.to_excel(filename_not_ocurrencies, index=False)
    for file in os.listdir("data/processed"):
        for contato in contatos:
            logger.info(f" Sending file {file} to {contato} via WhatsApp.")
            send_whatsapp(
                username=contato,
                file=os.path.join("data", "processed", file),
            )
    if filename_not_ocurrencies:
        [
            send_whatsapp(
                username=contato,
                file=filename_not_ocurrencies,
                message=f"""
> Clientes não correspondentes em Bordero\n 
Segue os Clientes (CNPJs/CPFs) de "_{os.path.basename(filename_rel_payments)}_" que não foram encontrados 
em Bordero.
""",
            )
            for contato in contatos
        ]
    logger.info("Finished processing files 'Pendencias' and 'Baixas'.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ["--debug",'-d']:
            main()
            sys.exit(0)
        else:
            logger.error(
                "[ERROR] Invalid argument. Use '--debug' to execute the script."
            )
            sys.exit(1)
    schedule.every().day.at("07:05").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
        print(
            f"{time.strftime('%X')} -  Waiting for the next scheduled run...",
            end="\r",
        )
