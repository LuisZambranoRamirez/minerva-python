from datetime import datetime
from decimal import Decimal
from typing import Final, List
import uuid

from domain.exceptions.domainException import DomainException 
from domain.constants.PaymentMethod import PaymentMethod
from domain.entities.customer.CustomerId import CustomerId
from domain.entities.product.ProductId import ProductId
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.sale.Pay import Pay
from domain.entities.sale.SaleDetail import SaleDetail
from domain.entities.shared.Money import Money

class Sale:
    def __init__(
        self, 
        customer_name_id: str, 
        first_product_id: str, 
        first_price_unit: Decimal, 
        first_quantity: Decimal
    ):
        # 1. Validar e instanciar el identificador del cliente
        if customer_name_id is None:
            raise DomainException("El cliente es requerido para iniciar una venta.")
        self._customer_id: Final[CustomerId] = CustomerId(customer_name_id)

        # 2. Inicializar colecciones internas
        self._sale_details: List[SaleDetail] = []
        self._pays: List[Pay] = []

        # 3. Datos iniciales automáticos de la entidad
        self._sale_id: Final[uuid.UUID] = uuid.uuid4()
        self._registration_date: Final[datetime] = datetime.now()

        # 4. Forzar la presencia de al menos un detalle válido para crear la venta
        self.add_detail(first_product_id, first_price_unit, first_quantity)

    def add_detail(self, product_id: str, price_unit: Decimal, quantity: Decimal) -> None:
        """Instancia los Value Objects requeridos y añade una nueva línea de detalle."""
        prod_id = ProductId(product_id)
        money_price = Money(price_unit)
        qty_product = ProductQuantity(quantity)

        # El constructor de SaleDetail ya ejecuta sus propias validaciones de negocio
        detail = SaleDetail(product_id=prod_id, quantity=qty_product, price_unit=money_price)
        self._sale_details.append(detail)

    def add_payment(self, amount: Decimal, payment_method: PaymentMethod) -> None:
        """Registra un pago parcial o total contra la deuda actual de la venta."""
        if self.is_due_canceled():
            raise DomainException("La VENTA ya está CANCELADA.")

        money_amount = Money(amount)
        
        # El constructor de Pay valida el monto mínimo y la presencia del método de pago
        pay_created = Pay(amount=money_amount, payment_method=payment_method)

        if pay_created.amount.value > self.calculate_amount_due():
            raise DomainException("El PAGO sobrepasa la DEUDA de la VENTA.")

        self._pays.append(pay_created)

    # --------------------- CÁLCULOS DE AGREGADO --------------------- OJOOOOOOOO, VER SI EL CALCULO DEL TOTAL ES VALIDO

    def calculate_total(self) -> Decimal:
        """Suma el subtotal de cada una de las líneas de detalle."""
        return sum((detail.calculate_total() for detail in self._sale_details), Decimal("0"))

    def calculate_total_paid(self) -> Decimal:
        """Suma todos los montos de los pagos registrados con éxito."""
        return sum((pay.amount.value for pay in self._pays), Decimal("0"))

    def calculate_amount_due(self) -> Decimal:
        """Devuelve el balance pendiente (Total - Pagado)."""
        return self.calculate_total() - self.calculate_total_paid()

    def is_due_canceled(self) -> bool:
        """Indica si el saldo pendiente ha sido liquidado por completo."""
        return self.calculate_amount_due() == Decimal("0")

    # --------------------- PROPIEDADES (GETTERS) ---------------------

    @property
    def id(self) -> uuid.UUID:
        return self._sale_id

    @property
    def registration_date(self) -> datetime:
        return self._registration_date

    @property
    def customer_id(self) -> str:
        return self._customer_id.value

    # Ofrecemos acceso de solo lectura a las listas para proteger la encapsulación del agregado
    @property
    def sale_details(self) -> List[SaleDetail]:
        return list(self._sale_details)

    @property
    def pays(self) -> List[Pay]:
        return list(self._pays)

    # --------------------- EQUALS & HASH POR IDENTIDAD ---------------------

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sale):
            return False
        return self._sale_id == other._sale_id

    def __hash__(self) -> int:
        return hash(self._sale_id)