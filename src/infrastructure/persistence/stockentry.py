class StockEntry(Base):

    __tablename__ = "stockEntry"

    stockEntryId = mapped_column(CHAR(36), primary_key=True)

    productNameId = mapped_column(
        ForeignKey("product.productNameId")
    )

    supplierNameId = mapped_column(
        ForeignKey("supplier.supplierNameId")
    )

    unitPrice = mapped_column(Numeric(10,2))

    quantity = mapped_column(Numeric(10,3))

    expirationDate = mapped_column(DateTime, nullable=True)

    registrationDate = mapped_column(DateTime)

    product = relationship("Product", back_populates="stockEntries")

    supplier = relationship("Supplier", back_populates="entries")