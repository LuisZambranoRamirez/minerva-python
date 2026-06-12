from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import product_router, supplier_router, customer_router

app = FastAPI(title="Minerva API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router.router, prefix="/api")
app.include_router(supplier_router.router, prefix="/api")
app.include_router(customer_router.router, prefix="/api")

from fastapi import Request
from fastapi.responses import JSONResponse
from domain.exceptions.DomainException import DomainException

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.get('/')
def home():
    return {"message": "Minerva API is running"}
