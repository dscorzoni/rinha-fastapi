from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Model


class CustomerModel(Model):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    limite = Column(Integer)
    saldo = Column(Integer, default=0)

    transacoes = relationship("TransactionModel", back_populates="cliente")


class TransactionModel(Model):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    valor = Column(Integer)
    tipo = Column(String)
    descricao = Column(String)
    realizada_em = Column(DateTime, server_default=func.now())

    cliente = relationship("CustomerModel", back_populates="transacoes")
