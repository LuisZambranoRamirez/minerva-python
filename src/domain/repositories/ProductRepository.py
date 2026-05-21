from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.product.product import Product
from domain.entities.product.product_id import ProductId
from domain.entities.product.bar_code import BarCode
from domain.entities.product.product_quantity import ProductQuantity
from domain.entities.stock_entry.stock_entry import StockEntry


class ProductRepository(ABC):

    @abstractmethod
    def save_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def save_stock_entry(self, stock_entry: StockEntry) -> None:
        pass

    @abstractmethod
    def save_unit_to_bulk(
        self,
        unit_product_id: ProductId,
        bulk_product_id: ProductId,
        quantity: ProductQuantity
    ) -> None:
        pass

    @abstractmethod
    def exists_by_id(self, product_id: ProductId) -> bool:
        pass

    @abstractmethod
    def exists_by_bar_code(self, bar_code: BarCode) -> bool:
        pass

    @abstractmethod
    def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        pass

    @abstractmethod
    def find_by_bar_code(self, bar_code: BarCode) -> Optional[Product]:
        pass

    @abstractmethod
    def find_latest_entry_before_today(
        self, product_id: ProductId
    ) -> Optional[StockEntry]:
        pass

    @abstractmethod
    def find_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def find_all_entries_by_product_id(
        self, product_id: ProductId
    ) -> List[StockEntry]:
        pass