from fastapi import APIRouter, HTTPException
from .schema import TransactionSchema
from .database import db_session
from .models import CustomerModel, TransactionModel
from sqlalchemy import select
import datetime

router = APIRouter()


@router.post("/clientes/{id}/transacoes")
async def post_transacoes(id: int, request: TransactionSchema):
    async with db_session.begin() as session:
        customer = await session.get(CustomerModel, id, with_for_update=True)
        if not customer:
            raise HTTPException(
                status_code=400,
                detail='Cliente não encontrado'
            )

        # Business Logic
        if request.tipo == 'd':
            new_balance = customer.saldo - request.valor
            if new_balance < (-customer.limite):
                raise HTTPException(
                    status_code=422,
                    detail='Limite insuficiente'
                )
        else:
            new_balance = customer.saldo + request.valor

        # Adding to the database and updating customer balance
        db_transaction = TransactionModel(
            valor=request.valor,
            tipo=request.tipo,
            descricao=request.descricao,
            customer_id=id
        )
        session.add(db_transaction)
        customer.saldo = new_balance
        return {"limite": customer.limite, "saldo": new_balance}


@router.get('/clientes/{id}/extrato')
async def get_extratos(id: int):
    async with db_session.begin() as session:
        customer = await session.get(CustomerModel, id)
        if not customer:
            raise HTTPException(
                status_code=404,
                detail='Cliente não encontrado'
            )
        last_transactions = await session.execute(
            select(TransactionModel)
            .where(TransactionModel.customer_id == id)
            .order_by(TransactionModel.id.desc())
            .limit(10)
        )
        last_transactions = last_transactions.scalars().all()
        clean_last_transactions = [
            {
                "valor": i.valor,
                "tipo": i.tipo,
                "descricao": i.descricao,
                "realizada_em": i.realizada_em
            } for i in last_transactions
        ]
        return {
            "saldo": {
                "total": customer.saldo,
                "data_extrato": datetime.datetime.now(),
                "limite": customer.limite
            },
            "ultimas_transacoes": clean_last_transactions
        }
