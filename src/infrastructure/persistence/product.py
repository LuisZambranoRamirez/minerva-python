class Product(Base):

    __tablename__ = "product"

    productNameId: Mapped[str] = mapped_column(String(100), primary_key=True)

    gainStrategy: Mapped[GainStrategyEnum] = mapped_column(Enum(GainStrategyEnum))

    gainAmount: Mapped[float] = mapped_column(Numeric(10,2))

    price: Mapped[float] = mapped_column(Numeric(10,2))

    stock: Mapped[float] = mapped_column(Numeric(10,3))

    reorderLevel: Mapped[float | None] = mapped_column(Numeric(10,3))

    barCode: Mapped[str | None] = mapped_column(CHAR(13), unique=True)

    saleType: Mapped[SaleTypeEnum] = mapped_column(Enum(SaleTypeEnum))

    category: Mapped[ProductCategoryEnum] = mapped_column(Enum(ProductCategoryEnum))

    registrationDate: Mapped = mapped_column(DateTime)

    stockEntries = relationship("StockEntry", back_populates="product")
    saleDetails = relationship("SaleDetail", back_populates="product")
    losses = relationship("InventoryLoss", back_populates="product")