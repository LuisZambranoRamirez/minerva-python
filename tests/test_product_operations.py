import sys
import unittest
from pathlib import Path
from decimal import Decimal

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from domain.constants.Category import Category
from domain.constants.GainStrategy import GainStrategy
from domain.constants.SaleType import SaleType
from domain.entities.product.Product import Product


class ProductOperationsTest(unittest.TestCase):

    def make_product(self, stock: Decimal) -> Product:
        return Product(
            product_name="Test Product",
            gain_strategy=GainStrategy.PORCENTAJE,
            gain_amount=Decimal("0.10"),
            reorder_level=None,
            bar_code="1234567890123",
            sale_type=SaleType.UNIDAD,
            initial_stock=stock,
            category=Category.OTROS,
            purchase_price=Decimal("100")
        )

    def test_process_inventory_loss_decreases_stock(self):
        product = self.make_product(Decimal("10"))

        result = product.process_inventory_loss(Decimal("2"))

        self.assertTrue(result.is_success())
        self.assertEqual(product.get_stock().value, Decimal("8"))

    def test_process_product_return_increases_stock(self):
        product = self.make_product(Decimal("10"))

        result = product.process_product_return(Decimal("2"))

        self.assertTrue(result.is_success())
        self.assertEqual(product.get_stock().value, Decimal("12"))


if __name__ == "__main__":
    unittest.main()
