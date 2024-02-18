from fastapi import FastAPI
from .models import Model
from .database import db_engine, db_session
from .models import CustomerModel
app = FastAPI()

# Creating database tables
Model.metadata.create_all(db_engine)

# Initialize Customer Data
# Check if customer_id = 1 exists


def add_customer_data():
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
