"""
Colunas de pendencias:
    `id`; `Valor da parcela`; `Documento`; `Valor_pendente`; `Emitente`; `C.N.P.J./C.P.F.`; `grupo_centro_de_custo`; `Centro de custo`.
Colunas de baixas:
    `data_baixa`; `id`; `valor`; `documento`; `emitente`; `cnpj_cpf`;`idcentro_custo`; `grupo_centro_custo`; `centro_custo` .
"""

from sqlalchemy import (
    Column,
    BigInteger,
    DateTime,
    Enum,
    String,
    DECIMAL,
    Date,
    func,
)
from models.base import Base


class Dtype:
    PENDENCIAS = "pendencias"
    BAIXAS = "baixas"


class Payments(Base):
    __tablename__ = "pendencias_baixas"
    id_pendencias_baixas = Column(
        BigInteger, primary_key=True, autoincrement=True
    )
    id = Column(BigInteger, nullable=False)
    valor_parcela = Column(DECIMAL(10, 2), nullable=False)
    documento = Column(String(60), nullable=False)
    valor_pendente = Column(DECIMAL(10, 2), nullable=False)
    emitente = Column(String(100), nullable=False)
    cnpj_cpf = Column(String(30), nullable=False)
    grupo_centro_de_custo = Column(String(50))
    centro_custo = Column(String(50))
    data_baixa = Column(Date)
    idcentro_custo = Column(BigInteger)
    filename = Column(String(100), nullable=True)
    dtype = Column(Enum("pendencias", "baixas", name="dtype"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    __mapper_args__ = {"confirm_deleted_rows": False}

    def __init__(
        self,
        id,
        valor_parcela,
        documento,
        valor_pendente,
        emitente,
        cnpj_cpf,
        grupo_centro_de_custo,
        centro_custo,
        data_baixa,
        idcentro_custo,
    ):
        self.id = id
        self.valor_parcela = valor_parcela
        self.documento = documento
        self.valor_pendente = valor_pendente
        self.emitente = emitente
        self.cnpj_cpf = cnpj_cpf
        self.grupo_centro_de_custo = grupo_centro_de_custo
        self.centro_custo = centro_custo
        self.data_baixa = data_baixa
        self.idcentro_custo = idcentro_custo
