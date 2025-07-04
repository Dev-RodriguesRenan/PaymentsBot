from models.base import Base
from models.conection import get_engine
from models.db_actions import create_pendencias_baixas

Base.metadata.create_all(get_engine())
create_pendencias_baixas(
    "data/RelatorioParcelasPendentes_20250703_1427.xlsx", 3
)
create_pendencias_baixas(
    "data/RelatorioRealizacoesBaixas_20250703_1408.xlsx", 4
)
