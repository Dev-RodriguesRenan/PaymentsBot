from contextlib import contextmanager
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("USUARIO")
password = os.getenv("SENHA")
host = os.getenv("NOME_DO_HOST")
database = os.getenv("BANCO_DE_DADOS")
show_sql = os.getenv("SHOW_SQL", "False")


def get_engine(
    username=username,
    password=password,
    host=host,
    database=database,
    echo=True if show_sql == "True" else False,
):
    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:3306/{database}",
        echo=echo,
    )


@contextmanager
def get_session(
    username=username, password=password, host=host, database=database
):
    engine = get_engine(
        username=username, password=password, host=host, database=database
    )
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
