from fastapi import FastAPI

from app.db.init_db import init_db
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.product import router as product_router
from app.api.v1.endpoints.order import router as order_router

init_db()

app = FastAPI(
    title="E-commerce API",
    description="API REST para gerenciamento de usuários, produtos e pedidos.",
    version="1.0.0",
    contact={
        "name": "Lucas"
    },
    license_info={
        "name": "MIT License"
    }
)


@app.get(
    "/",
    summary="Verificar status da API",
    description="Retorna uma mensagem confirmando que a E-commerce API está em funcionamento.",
    tags=["Status"]
)
def root():
    return {"message": "E-commerce API funcionando!"}


app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)