from infrastructure.persistence.session import init_database
from contextlib import asynccontextmanager
from fastapi import FastAPI
from infrastructure.api.exception_handlers import register_exception_handlers
from infrastructure.api.routers.customer_router import router as customer_router
from infrastructure.api.routers.login_router import router as login_router
from infrastructure.api.routers.product_router import router as product_router
from infrastructure.api.routers.sale_router import router as sale_router
from infrastructure.api.routers.supplier_router import router as supplier_router

#from infrastructure.api.routers.product_router import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
    
app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

@app.get('/')
def home():
    return "hola mundo"

app.include_router(login_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(sale_router)
app.include_router(supplier_router)
