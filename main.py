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
        subprocess.run(["python", "-m", "robot", "-d", "results", path_file])
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
    # execute all robot files in the suites directory
    for folder in os.listdir("suites"):
        for file in os.listdir(f"suites/{folder}"):
            if file.endswith(".robot"):
                run_file(f"suites/{folder}/{file}")
    logger.info("Database and tables created successfully.")
    # check if the data directory exists and create pendencias baixas
    for file in os.listdir("data"):
        if file.endswith(".xlsx"):
            logger.info(f" Processing file: {file}")
            header = 4 if "RealizacoesBaixas" in file else 3
            create_pendencias_baixas(f"data/{file}", header)
            logger.info(f" File {file} processed successfully.")
    # generate payments dataframe, export in excel file and send by whatsApp
    dataframe = payments_df_generator()
    if dataframe.empty:
        logger.warning("[WARNING] No data found in the database.")
        drop_all_payments()
        return
    dataframe.to_excel(
        f"data/processed/RelatorioDePagamentos_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        index=False,
    )
    for file in os.listdir("data/processed"):
        for contato in contatos:
            send_whatsapp(
                username=contato,
                file=os.path.join("data", "processed", file),
            )
    # clear database payments table
    drop_all_payments()
    logger.info("Finished processing files 'Pendencias' and 'Baixas'.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--debug":
            main()
            sys.exit(0)
        else:
            logger.error(
                "[ERROR] Invalid argument. Use '--debug' to execute the script."
            )
            sys.exit(1)
    schedule.every().day.at("06:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
        print(
            f"{time.strftime('%X')} -  Waiting for the next scheduled run...",
            end="\r",
        )
