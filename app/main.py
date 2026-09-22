from fastapi import FastAPI

from app.db.init_db import init_db
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.product import router as product_router

init_db()

app = FastAPI(title="E-commerce API")


@app.get("/")
def root():
    return {"message": "E-commerce API funcionando!"}


app.include_router(user_router)
app.include_router(product_router)