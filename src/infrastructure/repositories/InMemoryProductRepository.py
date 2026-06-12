from typing import List, Optional, Dict

from domain.entities.product.Product import Product
from domain.entities.product.ProductId import ProductId
from domain.entities.product.BarCode import BarCode
from domain.entities.product.ProductQuantity import ProductQuantity
from domain.entities.product.StockEntry import StockEntry
from domain.repositories.ProductRepository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._stock_entries: List[StockEntry] = []

    def save_product(self, product: Product) -> None:
        self._products[product.product_name_id.value] = product

    def save_stock_entry(self, stock_entry: StockEntry) -> None:
        self._stock_entries.append(stock_entry)

    def save_unit_to_bulk(self, unit_product_id: ProductId, bulk_product_id: ProductId, quantity: ProductQuantity) -> None:
        pass # Not used yet in UI

    def exists_by_id(self, product_id: ProductId) -> bool:
        return product_id.value in self._products

    def exists_by_bar_code(self, bar_code: BarCode) -> bool:
        return any(p.bar_code and p.bar_code.value == bar_code.value for p in self._products.values())

    def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        return self._products.get(product_id.value)

    def find_by_bar_code(self, bar_code: BarCode) -> Optional[Product]:
        for p in self._products.values():
            if p.bar_code and p.bar_code.value == bar_code.value:
                return p
        return None

    def find_latest_entry_before_today(self, product_id: ProductId) -> Optional[StockEntry]:
        return None

    def find_all_products(self) -> List[Product]:
        return list(self._products.values())

    def find_all_entries_by_product_id(self, product_id: ProductId) -> List[StockEntry]:
        return [se for se in self._stock_entries if se.product_id.value == product_id.value]

    def delete_by_id(self, product_id: ProductId) -> None:
        if product_id.value in self._products:
            del self._products[product_id.value]
