class Supplier(Base):

    __tablename__ = "supplier"

    supplierNameId: Mapped[str] = mapped_column(String(100), primary_key=True)

    ruc: Mapped[str | None] = mapped_column(CHAR(11), unique=True)

    phoneNumber: Mapped[str | None] = mapped_column(CHAR(9), unique=True)

    registrationDate: Mapped = mapped_column(DateTime)

    entries = relationship("StockEntry", back_populates="supplier")