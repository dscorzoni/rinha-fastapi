from fastapi import FastAPI
from .models import Model, CustomerModel
from .routes import router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

app = FastAPI()
app.include_router(router)


def add_customer_data():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres@db/postgres"

    db_engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_size=30,
        max_overflow=0,
        isolation_level="AUTOCOMMIT"
    )

    db_session = scoped_session(sessionmaker(
        bind=db_engine,
        autoflush=False,
        future=True
    ))

    # Creating database tables
    Model.metadata.create_all(db_engine)

    # Adding customer data
    customer1 = db_session.query(CustomerModel).filter(
        CustomerModel.id == 1).first()

    if not customer1:
        # Add base customer data
        limits = [100000, 80000, 1000000, 10000000, 500000]
        for limit in limits:
            db_customer = CustomerModel(limite=limit)
            db_session.add(db_customer)
            db_session.commit()
            db_session.refresh(db_customer)

        print('====== Cadastro Basico de Clientes Realizado ======')


add_customer_data()


@app.get("/")
def read_root():
    return {"Hello": "World"}
