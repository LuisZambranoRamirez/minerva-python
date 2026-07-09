from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum,
    Numeric,
    ForeignKey,
    CHAR
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "user"

    userName: Mapped[str] = mapped_column(String(30), primary_key=True)
    DNI: Mapped[str] = mapped_column(CHAR(8), unique=True)
    names: Mapped[str] = mapped_column(String(50))
    lastNames: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    roleName: Mapped[str] = mapped_column(String(50))
    isActive: Mapped[bool] = mapped_column(Boolean)
    registrationDate: Mapped = mapped_column(DateTime)

    actions = relationship("UserAction", back_populates="user")