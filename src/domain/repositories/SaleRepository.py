from domain.entities.sale import DTO
from abc import ABC, abstractmethod
from typing import List, Optional, Set

from domain.entities.customer.CustomerId import CustomerId
from domain.entities.product.Product import Product
from domain.entities.sale.PayId import PayId
from domain.entities.sale.SaleDetailId import SaleDetailId
from domain.entities.sale.SaleId import SaleId
from domain.entities.sale.Sale import Sale


class SaleRepository(ABC):

    @abstractmethod
    def save(
        self,
        sale: Sale,
        products: Set[Product]
    ) -> None:
        pass

    @abstractmethod
    def find_by_id(
        self,
        id: SaleId
    ) -> Optional[Sale]:
        pass

    @abstractmethod
    def find_by_customer_id(
        self,
        customer_id: CustomerId
    ) -> List[Sale]:
        pass

    @abstractmethod
    def find_all(self) -> List[Sale]:
        pass

    @abstractmethod
    def find_sale_details_by_id(
        self,
        id: SaleDetailId
    ) -> List[DTO.SaleDetailDTO]:
        pass

    @abstractmethod
    def find_pays_by_id(
        self,
        id: PayId
    ) -> List[DTO.PayDTO]:
        pass

    @abstractmethod
    def update_payments(
        self,
        sale: Sale
    ) -> None:
        pass