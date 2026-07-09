class Customer(Base):

    __tablename__ = "customer"

    customerNameId: Mapped[str] = mapped_column(String(50), primary_key=True)

    phoneNumber: Mapped[str | None] = mapped_column(CHAR(9), unique=True)

    registrationDate: Mapped = mapped_column(DateTime)

    sales = relationship("Sale", back_populates="customer")