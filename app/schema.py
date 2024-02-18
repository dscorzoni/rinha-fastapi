from pydantic import BaseModel, field_validator
from fastapi import HTTPException


class CustomerSchema(BaseModel):
    id: int
    limite: int
    saldo: int


class TransactionSchema(BaseModel):
    valor: int
    tipo: str
    descricao: str

    # Validations: valor
    @field_validator("valor")
    @classmethod
    def ensure_positive(cls, value):
        if value <= 0:
            raise HTTPException(
                status_code=422,
                detail="O campo valor precisa ser maior que zero"
            )
        return value

    # Validations: tipo
    @field_validator("tipo")
    @classmethod
    def ensure_credit_debit(cls, value):
        if value not in ['c', 'd']:
            raise HTTPException(
                status_code=422,
                detail='O campo tipo precisa ser "d" or "c".'
            )
        return value

    # Validations: descricao
    @field_validator("descricao")
    @classmethod
    def ensure_ten_chars(cls, value):
        if len(value) > 10 or len(value) == 0:
            raise HTTPException(
                status_code=422,
                detail='O campo descrição pode ter entre 1 e 10 caracteres.'
            )
        return value
