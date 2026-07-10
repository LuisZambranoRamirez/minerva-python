from fastapi import FastAPI
from infrastructure.api.exception_handlers import register_exception_handlers
from infrastructure.api.routers.customer_router import router as customer_router
from infrastructure.api.routers.login_router import router as login_router

#from infrastructure.api.routers.product_router import router as product_router

app = FastAPI()

register_exception_handlers(app)

@app.get('/')
def home():
    return "hola mundo"

app.include_router(login_router)
app.include_router(customer_router)
