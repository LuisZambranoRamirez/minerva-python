from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return "hola mundo"

from fastapi import FastAPI

from infra.api.exception_handlers import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(customer_router)
app.include_router(product_router)