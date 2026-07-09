class UserAction(Base):
    __tablename__ = "userAction"

    userActionId: Mapped[str] = mapped_column(CHAR(36), primary_key=True)

    userName: Mapped[str] = mapped_column(
        ForeignKey("user.userName", onupdate="CASCADE", ondelete="RESTRICT")
    )

    permission: Mapped[str] = mapped_column(String(50))

    entityId: Mapped[str] = mapped_column(String(100))

    registrationDate: Mapped = mapped_column(DateTime)

    user = relationship("User", back_populates="actions")