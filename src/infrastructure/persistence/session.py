import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("POSTGRES_URL_NON_POOLING")


if not DATABASE_URL:
    print("POSTGRES_URL_NON_POOLING no configurada. Iniciando con base de datos local.")
    DATABASE_URL = "postgresql+psycopg://postgres:Drakotako147258369#@localhost/apolo"

else:
    print("Conectando a Supabase PostgreSQL")

    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+psycopg://"
    ).replace(
        "postgresql://",
        "postgresql+psycopg://"
    )


# SQLAlchemy necesita el driver psycopg
DATABASE_URL = DATABASE_URL.replace(
    "postgres://",
    "postgresql+psycopg://"
).replace(
    "postgresql://",
    "postgresql+psycopg://"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)