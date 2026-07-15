from abc import ABC, abstractmethod
from typing import List, Optional, Set

from domain.entities.product.InventoryLoss import InventoryLoss
from domain.entities.product.Product import Product
from domain.entities.product.ProductId import ProductId
from domain.entities.sale.ProductReturn import ProductReturn
from domain.entities.stockEntry.StockEntry import StockEntry
from domain.valueObject.BarCode import BarCode
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName


class ProductRepository(ABC):

    @abstractmethod
    def register_product(
        self,
        product: Product,
        stock_entry: StockEntry
    ) -> None:
        pass

    @abstractmethod
    def save(
        self,
        product: Product
    ) -> None:
        pass

    @abstractmethod
    def save_stock_entry(
        self,
        stock_entry: StockEntry,
        product: Product
    ) -> None:
        pass

    @abstractmethod
    def save_unit_to_bulk(
        self,
        unit_product_name: ProductName,
        bulk_product_name: ProductName,
        quantity: ProductQuantity
    ) -> None:
        pass

    @abstractmethod
    def save_inventory_loss(
        self,
        inventory_loss: InventoryLoss,
        product: Product
    ) -> None:
        pass

    @abstractmethod
    def save_product_return(
        self,
        product_return: ProductReturn,
        product: Product
    ) -> None:
        pass

    @abstractmethod
    def exists_by_id(
        self,
        id: ProductId
    ) -> bool:
        pass

    @abstractmethod
    def exists_by_bar_code(
        self,
        bar_code: BarCode
    ) -> bool:
        pass

    @abstractmethod
    def find_by_id(
        self,
        id: ProductId
    ) -> Optional[Product]:
        pass

    @abstractmethod
    def find_by_bar_code(
        self,
        bar_code: BarCode
    ) -> Optional[Product]:
        pass

    @abstractmethod
    def find_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def find_all_entries_by_product_id(
        self,
        id: ProductId
    ) -> List[StockEntry]:
        pass

    @abstractmethod
    def find_all_by_ids(
        self,
        product_ids: Set[ProductId]
    ) -> Set[Product]:
        pass