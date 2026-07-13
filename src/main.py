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

# Cleaned up debug routes
import uuid
import datetime
from sqlalchemy import text
from infrastructure.persistence.session import SessionLocal

@app.post("/debug/populate-db")
def populate_db():
    db = SessionLocal()
    try:
        # Clear existing tables first to avoid conflict and have clean data
        db.execute(text("TRUNCATE TABLE productreturn, saledetail, pay, sale, stockentry, product, supplier, customer RESTART IDENTITY CASCADE;"))
        
        # Suppliers
        suppliers = [
            ("Distribuidora San Jose", "20123456789", "987654321"),
            ("Alicorp", "20987654321", "912345678"),
            ("Gloria S.A.", "20444555666", "999888777"),
            ("Nestle Peru", "20555666777", "955444333")
        ]
        for name, ruc, phone in suppliers:
            db.execute(
                text("INSERT INTO supplier (suppliernameid, registrationdate, ruc, phonenumber) VALUES (:name, :reg, :ruc, :phone)"),
                {"name": name, "reg": datetime.datetime(2025, 12, 1, 10, 0), "ruc": ruc, "phone": phone}
            )

        # Customers
        customers = [
            ("Juan Perez", "944555666"),
            ("Maria Rodriguez", "911222333"),
            ("Carlos Mendoza", "933444555"),
            ("Ana Torres", "988777666"),
            ("Lucia Gomez", "922333444")
        ]
        for name, phone in customers:
            db.execute(
                text("INSERT INTO customer (customernameid, registrationdate, phonenumber) VALUES (:name, :reg, :phone)"),
                {"name": name, "reg": datetime.datetime(2025, 12, 1, 10, 0), "phone": phone}
            )

        # Products
        products = [
            ("Arroz Costeno 1kg", "INCREMENTAL", 1.50, 4.70, 80, "UNIDAD", "ABARROTES_SECOS", 10, "7750123456789", "Distribuidora San Jose", 3.20),
            ("Coca Cola 15L", "INCREMENTAL", 1.20, 5.70, 60, "UNIDAD", "BEBIDAS", 5, "7750987654321", "Distribuidora San Jose", 4.50),
            ("Leche Gloria 400g", "INCREMENTAL", 1.00, 4.20, 100, "UNIDAD", "LACTEOS", 15, "7750111222333", "Gloria S.A.", 3.20),
            ("Aceite Primor 1L", "INCREMENTAL", 2.00, 10.50, 40, "UNIDAD", "ABARROTES_SECOS", 8, "7750222333444", "Alicorp", 8.50),
            ("Cafe Altomayo 200g", "INCREMENTAL", 3.00, 14.50, 30, "UNIDAD", "CAFE_INFUSIONES", 5, "7750333444555", "Distribuidora San Jose", 11.50),
            ("Chocolate Sublime", "INCREMENTAL", 0.70, 2.50, 150, "UNIDAD", "SNACKS_GOLOSINAS", 20, "7750444555666", "Nestle Peru", 1.80),
            ("Detergente Opal 1kg", "INCREMENTAL", 1.80, 9.80, 25, "UNIDAD", "LIMPIEZA_HOGAR", 5, "7750555666777", "Alicorp", 8.00),
            ("Comida Ricocan 2kg", "INCREMENTAL", 4.00, 21.00, 15, "UNIDAD", "MASCOTAS", 3, "7750666777888", "Distribuidora San Jose", 17.00)
        ]
        for name, gain_strat, gain_amt, price, stock, s_type, cat, reorder, barcode, supplier, p_price in products:
            db.execute(
                text("INSERT INTO product (productnameid, gainstrategy, gainamount, price, stock, saletype, category, registrationdate, reorderlevel, barcode) VALUES (:name, :gain_strat, :gain_amt, :price, :stock, :s_type, :cat, :reg, :reorder, :barcode)"),
                {"name": name, "gain_strat": gain_strat, "gain_amt": gain_amt, "price": price, "stock": stock, "s_type": s_type, "cat": cat, "reg": datetime.datetime(2025, 12, 5, 11, 0), "reorder": reorder, "barcode": barcode}
            )
            se_id = str(uuid.uuid4())
            db.execute(
                text("INSERT INTO stockentry (stockentryid, productnameid, suppliernameid, unitprice, quantity, registrationdate, expirationdate) VALUES (:se_id, :prod_name, :sup_name, :u_price, :qty, :reg, :exp)"),
                {"se_id": se_id, "prod_name": name, "sup_name": supplier, "u_price": p_price, "qty": stock + 20, "reg": datetime.datetime(2025, 12, 5, 11, 0), "exp": datetime.datetime(2027, 12, 31, 0, 0)}
            )

        # Sales spread from January to July 2026
        sales_data = [
            ("Juan Perez", 1, 15, [("Arroz Costeno 1kg", 5, 4.70), ("Coca Cola 15L", 2, 5.70)], "EFECTIVO"),
            ("Maria Rodriguez", 2, 10, [("Leche Gloria 400g", 10, 4.20)], "DIGITAL"),
            ("Carlos Mendoza", 3, 22, [("Cafe Altomayo 200g", 2, 14.50)], "EFECTIVO"),
            ("Ana Torres", 4, 5, [("Aceite Primor 1L", 4, 10.50), ("Arroz Costeno 1kg", 4, 4.70)], "DIGITAL"),
            ("Lucia Gomez", 5, 18, [("Chocolate Sublime", 5, 2.50), ("Coca Cola 15L", 1, 5.70)], "EFECTIVO"),
            ("Juan Perez", 6, 25, [("Detergente Opal 1kg", 3, 9.80), ("Leche Gloria 400g", 6, 4.20)], "DIGITAL"),
            ("Maria Rodriguez", 7, 2, [("Comida Ricocan 2kg", 2, 21.00), ("Aceite Primor 1L", 2, 10.50)], "EFECTIVO"),
            ("Ana Torres", 7, 5, [("Cafe Altomayo 200g", 4, 14.50), ("Chocolate Sublime", 10, 2.50)], "DIGITAL"),
            ("Carlos Mendoza", 7, 8, [("Arroz Costeno 1kg", 6, 4.70), ("Leche Gloria 400g", 4, 4.20)], "EFECTIVO"),
            ("Lucia Gomez", 7, 11, [("Detergente Opal 1kg", 2, 9.80), ("Coca Cola 15L", 2, 5.70)], "DIGITAL")
        ]

        for cust_name, m, d, items, pay_method in sales_data:
            s_id = str(uuid.uuid4())
            s_date = datetime.datetime(2026, m, d, 14, 30)
            db.execute(
                text("INSERT INTO sale (saleid, customernameid, registrationdate) VALUES (:s_id, :cust_name, :reg)"),
                {"s_id": s_id, "cust_name": cust_name, "reg": s_date}
            )
            total_amount = 0
            for prod_name, qty, u_price in items:
                sd_id = str(uuid.uuid4())
                subtotal = qty * u_price
                total_amount += subtotal
                db.execute(
                    text("INSERT INTO saledetail (saledetailid, saleid, productnameid, quantity, unitprice) VALUES (:sd_id, :s_id, :prod_name, :qty, :u_price)"),
                    {"sd_id": sd_id, "s_id": s_id, "prod_name": prod_name, "qty": qty, "u_price": u_price}
                )
                db.execute(
                    text("UPDATE product SET stock = stock - :qty WHERE productnameid = :prod_name"),
                    {"qty": qty, "prod_name": prod_name}
                )
            p_id = str(uuid.uuid4())
            db.execute(
                text("INSERT INTO pay (payid, saleid, amount, paymentmethod, registrationdate) VALUES (:p_id, :s_id, :amount, :pay_method, :reg)"),
                {"p_id": p_id, "s_id": s_id, "amount": total_amount, "pay_method": pay_method, "reg": s_date}
            )

        db.commit()
        return {"message": "Database populated with clean historical data."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()
