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


from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

@app.get('/')
def home():
    return "hola mundo"

app.include_router(login_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(sale_router)
app.include_router(supplier_router)

from sqlalchemy import text
from infrastructure.persistence.session import SessionLocal
import datetime

@app.post("/debug/update-sales-dates")
def update_sales_dates():
    db = SessionLocal()
    try:
        sales = db.execute(text("SELECT saleid FROM sale")).fetchall()
        months = [1, 2, 3, 4, 5, 6, 7]
        for idx, row in enumerate(sales):
            sale_id = row[0]
            month = months[idx % len(months)]
            new_date = datetime.datetime(2026, month, 12, 12, 0, 0)
            db.execute(
                text("UPDATE sale SET registrationdate = :new_date WHERE saleid = :sale_id"),
                {"new_date": new_date, "sale_id": sale_id}
            )
            db.execute(
                text("UPDATE pay SET registrationdate = :new_date WHERE saleid = :sale_id"),
                {"new_date": new_date, "sale_id": sale_id}
            )
        db.commit()
        return {"message": f"Updated {len(sales)} sales dates."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
