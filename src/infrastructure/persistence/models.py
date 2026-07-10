from typing import Optional
import datetime
import decimal
import enum

from sqlalchemy import Boolean, CHAR, DateTime, Enum, ForeignKeyConstraint, Numeric, PrimaryKeyConstraint, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class GainStrategyEnum(str, enum.Enum):
    PORCENTAJE = 'PORCENTAJE'
    INCREMENTAL = 'INCREMENTAL'


class LossReasonEnum(str, enum.Enum):
    DAÑADO = 'DAÑADO'
    VENCIMIENTO = 'VENCIMIENTO'
    PERDIDO = 'PERDIDO'
    COMSUMO = 'COMSUMO'
    ROBO = 'ROBO'
    OTROS = 'OTROS'


class PaymentMethodEnum(str, enum.Enum):
    EFECTIVO = 'EFECTIVO'
    DIGITAL = 'DIGITAL'


class ProductCategoryEnum(str, enum.Enum):
    BEBIDAS = 'BEBIDAS'
    ABARROTES_SECOS = 'ABARROTES_SECOS'
    CAFE_INFUSIONES = 'CAFE_INFUSIONES'
    LACTEOS = 'LACTEOS'
    CARNES = 'CARNES'
    SNACKS_GOLOSINAS = 'SNACKS_GOLOSINAS'
    CUIDADO_PERSONAL = 'CUIDADO_PERSONAL'
    LIMPIEZA_HOGAR = 'LIMPIEZA_HOGAR'
    BEBÉS = 'BEBÉS'
    MASCOTAS = 'MASCOTAS'
    OTROS = 'OTROS'


class ReturnReasonEnum(str, enum.Enum):
    DAÑADO = 'DAÑADO'
    VENCIDO = 'VENCIDO'
    EQUIVOCACION = 'EQUIVOCACION'
    OTROS = 'OTROS'


class SaleTypeEnum(str, enum.Enum):
    UNIDAD = 'UNIDAD'
    GRANEL = 'GRANEL'


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = (
        PrimaryKeyConstraint('customernameid', name='customer_pkey'),
        UniqueConstraint('phonenumber', name='customer_phonenumber_key')
    )

    customernameid: Mapped[str] = mapped_column(String(50), primary_key=True)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    phonenumber: Mapped[Optional[str]] = mapped_column(CHAR(9))

    sale: Mapped[list['Sale']] = relationship('Sale', back_populates='customer')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        PrimaryKeyConstraint('productnameid', name='product_pkey'),
        UniqueConstraint('barcode', name='product_barcode_key')
    )

    productnameid: Mapped[str] = mapped_column(String(100), primary_key=True)
    gainstrategy: Mapped[GainStrategyEnum] = mapped_column(Enum(GainStrategyEnum, values_callable=lambda cls: [member.value for member in cls], name='gain_strategy_enum'), nullable=False)
    gainamount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    saletype: Mapped[SaleTypeEnum] = mapped_column(Enum(SaleTypeEnum, values_callable=lambda cls: [member.value for member in cls], name='sale_type_enum'), nullable=False)
    category: Mapped[ProductCategoryEnum] = mapped_column(Enum(ProductCategoryEnum, values_callable=lambda cls: [member.value for member in cls], name='product_category_enum'), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    reorderlevel: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 3))
    barcode: Mapped[Optional[str]] = mapped_column(CHAR(13))

    inventoryloss: Mapped[list['Inventoryloss']] = relationship('Inventoryloss', back_populates='product')
    stockentry: Mapped[list['Stockentry']] = relationship('Stockentry', back_populates='product')
    unittobulk_bulkproductnameid: Mapped['Unittobulk'] = relationship('Unittobulk', uselist=False, foreign_keys='[Unittobulk.bulkproductnameid]', back_populates='product_bulkproductnameid')
    unittobulk_unitproductnameid: Mapped[list['Unittobulk']] = relationship('Unittobulk', foreign_keys='[Unittobulk.unitproductnameid]', back_populates='product')
    saledetail: Mapped[list['Saledetail']] = relationship('Saledetail', back_populates='product')


class Supplier(Base):
    __tablename__ = 'supplier'
    __table_args__ = (
        PrimaryKeyConstraint('suppliernameid', name='supplier_pkey'),
        UniqueConstraint('phonenumber', name='supplier_phonenumber_key'),
        UniqueConstraint('ruc', name='supplier_ruc_key')
    )

    suppliernameid: Mapped[str] = mapped_column(String(100), primary_key=True)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ruc: Mapped[Optional[str]] = mapped_column(CHAR(11))
    phonenumber: Mapped[Optional[str]] = mapped_column(CHAR(9))

    stockentry: Mapped[list['Stockentry']] = relationship('Stockentry', back_populates='supplier')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        PrimaryKeyConstraint('username', name='user_pkey'),
        UniqueConstraint('dni', name='user_dni_key')
    )

    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    dni: Mapped[str] = mapped_column(CHAR(8), nullable=False)
    names: Mapped[str] = mapped_column(String(50), nullable=False)
    lastnames: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    rolename: Mapped[str] = mapped_column(String(50), nullable=False)
    isactive: Mapped[bool] = mapped_column(Boolean, nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    useraction: Mapped[list['Useraction']] = relationship('Useraction', back_populates='user')


class Inventoryloss(Base):
    __tablename__ = 'inventoryloss'
    __table_args__ = (
        ForeignKeyConstraint(['productnameid'], ['product.productnameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_inventoryloss_product'),
        PrimaryKeyConstraint('inventorylossid', name='inventoryloss_pkey')
    )

    inventorylossid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    productnameid: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    reason: Mapped[LossReasonEnum] = mapped_column(Enum(LossReasonEnum, values_callable=lambda cls: [member.value for member in cls], name='loss_reason_enum'), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    observation: Mapped[Optional[str]] = mapped_column(String(255))

    product: Mapped['Product'] = relationship('Product', back_populates='inventoryloss')


class Sale(Base):
    __tablename__ = 'sale'
    __table_args__ = (
        ForeignKeyConstraint(['customernameid'], ['customer.customernameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_sale_customernameid'),
        PrimaryKeyConstraint('saleid', name='sale_pkey')
    )

    saleid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    customernameid: Mapped[str] = mapped_column(String(100), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    customer: Mapped['Customer'] = relationship('Customer', back_populates='sale')
    pay: Mapped[list['Pay']] = relationship('Pay', back_populates='sale')
    saledetail: Mapped[list['Saledetail']] = relationship('Saledetail', back_populates='sale')


class Stockentry(Base):
    __tablename__ = 'stockentry'
    __table_args__ = (
        ForeignKeyConstraint(['productnameid'], ['product.productnameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_stockentry_product'),
        ForeignKeyConstraint(['suppliernameid'], ['supplier.suppliernameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_stockentry_supplier'),
        PrimaryKeyConstraint('stockentryid', name='stockentry_pkey')
    )

    stockentryid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    productnameid: Mapped[str] = mapped_column(String(100), nullable=False)
    suppliernameid: Mapped[str] = mapped_column(String(100), nullable=False)
    unitprice: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    expirationdate: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)

    product: Mapped['Product'] = relationship('Product', back_populates='stockentry')
    supplier: Mapped['Supplier'] = relationship('Supplier', back_populates='stockentry')


class Unittobulk(Base):
    __tablename__ = 'unittobulk'
    __table_args__ = (
        ForeignKeyConstraint(['bulkproductnameid'], ['product.productnameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_bulk_product'),
        ForeignKeyConstraint(['unitproductnameid'], ['product.productnameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_unit_product'),
        PrimaryKeyConstraint('bulkproductnameid', 'unitproductnameid', name='unittobulk_pkey'),
        UniqueConstraint('bulkproductnameid', name='unittobulk_bulkproductnameid_key')
    )

    unitproductnameid: Mapped[str] = mapped_column(String(100), primary_key=True)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    bulkproductnameid: Mapped[str] = mapped_column(String(100), primary_key=True)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    product_bulkproductnameid: Mapped['Product'] = relationship('Product', foreign_keys=[bulkproductnameid], back_populates='unittobulk_bulkproductnameid')
    product: Mapped['Product'] = relationship('Product', foreign_keys=[unitproductnameid], back_populates='unittobulk_unitproductnameid')


class Useraction(Base):
    __tablename__ = 'useraction'
    __table_args__ = (
        ForeignKeyConstraint(['username'], ['user.username'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_useraction_user'),
        PrimaryKeyConstraint('useractionid', name='useraction_pkey')
    )

    useractionid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    permission: Mapped[str] = mapped_column(String(50), nullable=False)
    entityid: Mapped[str] = mapped_column(String(100), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='useraction')


class Pay(Base):
    __tablename__ = 'pay'
    __table_args__ = (
        ForeignKeyConstraint(['saleid'], ['sale.saleid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_pay_sale'),
        PrimaryKeyConstraint('payid', name='pay_pkey')
    )

    payid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    saleid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    paymentmethod: Mapped[PaymentMethodEnum] = mapped_column(Enum(PaymentMethodEnum, values_callable=lambda cls: [member.value for member in cls], name='payment_method_enum'), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    sale: Mapped['Sale'] = relationship('Sale', back_populates='pay')


class Saledetail(Base):
    __tablename__ = 'saledetail'
    __table_args__ = (
        ForeignKeyConstraint(['productnameid'], ['product.productnameid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_sd_product'),
        ForeignKeyConstraint(['saleid'], ['sale.saleid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_sd_sale'),
        PrimaryKeyConstraint('saledetailid', name='saledetail_pkey')
    )

    saledetailid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    saleid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    productnameid: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    unitprice: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    product: Mapped['Product'] = relationship('Product', back_populates='saledetail')
    sale: Mapped['Sale'] = relationship('Sale', back_populates='saledetail')
    productreturn: Mapped[list['Productreturn']] = relationship('Productreturn', back_populates='saledetail')


class Productreturn(Base):
    __tablename__ = 'productreturn'
    __table_args__ = (
        ForeignKeyConstraint(['saledetailid'], ['saledetail.saledetailid'], ondelete='RESTRICT', onupdate='CASCADE', name='fk_return_sale'),
        PrimaryKeyConstraint('productreturnid', name='productreturn_pkey')
    )

    productreturnid: Mapped[str] = mapped_column(CHAR(36), primary_key=True)
    saledetailid: Mapped[str] = mapped_column(CHAR(36), nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    reason: Mapped[ReturnReasonEnum] = mapped_column(Enum(ReturnReasonEnum, values_callable=lambda cls: [member.value for member in cls], name='return_reason_enum'), nullable=False)
    registrationdate: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)

    saledetail: Mapped['Saledetail'] = relationship('Saledetail', back_populates='productreturn')
