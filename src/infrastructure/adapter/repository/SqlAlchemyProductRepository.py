from domain.entities.product.InventoryLoss import InventoryLoss as DomainInventoryLoss
from domain.entities.product.Product import Product as DomainProduct
from domain.entities.product.ProductId import ProductId
from domain.entities.sale.ProductReturn import ProductReturn as DomainProductReturn
from domain.entities.stockEntry.StockEntry import StockEntry as DomainStockEntry

from domain.repositories.ProductRepository import ProductRepository

from domain.valueObject.BarCode import BarCode
from domain.valueObject.ProductQuantity import ProductQuantity
from domain.valueObject.id.ProductName import ProductName

from infrastructure.persistence.models import (
    Inventoryloss as InventoryLossModel,
    Product as ProductModel,
    Productreturn as ProductReturnModel,
    Stockentry as StockEntryModel,
    Unittobulk as UnitToBulkModel
)

from sqlalchemy.orm import Session

from typing import Optional, List, Set
from decimal import Decimal

class SqlAlchemyProductRepository(ProductRepository):

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    def register_product(
        self,
        product: DomainProduct,
        stock_entry: DomainStockEntry
    ) -> None:

        self.save(product)

        self.save_stock_entry(
            stock_entry,
            product
        )


    def save(
        self,
        product: DomainProduct
    ) -> None:

        model = ProductModel(
            productnameid=product.get_name_id().value,
            gainstrategy=product.get_gain_strategy(),
            gainamount=product.get_gain_amount().value,
            price=product.get_price().value,
            stock=product.get_stock().value,
            saletype=product.get_sale_type(),
            category=product.get_category(),
            registrationdate=product.get_registration_date(),
            reorderlevel = (
                lvl.value 
                if (lvl := product.get_reorder_level()) is not None 
                else None
            ),
            barcode = (
                bc.value 
                if (bc := product.get_bar_code()) is not None 
                else None
            )
        )

        self.session.merge(model)
        self.session.commit()

    def save_stock_entry(
        self,
        stock_entry: DomainStockEntry,
        product: DomainProduct
    ) -> None:

        model = StockEntryModel(
            stockentryid=stock_entry.id.as_string(),
            productnameid=product._product_name.as_string(),
            suppliernameid=stock_entry.supplier_name.value,
            unitprice=stock_entry.unit_price.value,
            quantity=stock_entry.quantity.value,
            registrationdate=stock_entry.registration_date,
            expirationdate=stock_entry.expiration_date
        )

        productModel = ProductModel(
            productnameid=product.get_name_id().value,
            gainstrategy=product.get_gain_strategy(),
            gainamount=product.get_gain_amount().value,
            price=product.get_price().value,
            stock=product.get_stock().value,
            saletype=product.get_sale_type(),
            category=product.get_category(),
            registrationdate=product.get_registration_date(),
            reorderlevel = (
                lvl.value 
                if (lvl := product.get_reorder_level()) is not None 
                else None
            ),
            barcode = (
                bc.value 
                if (bc := product.get_bar_code()) is not None 
                else None
            )
        )

        self.session.merge(productModel)
        self.session.add(model)
        self.session.commit()


    def save_unit_to_bulk(
        self,
        unit_product_name: ProductName,
        bulk_product_name: ProductName,
        quantity: ProductQuantity
    ) -> None:

        model = UnitToBulkModel(
            unitproductnameid=unit_product_name.value,
            bulkproductnameid=bulk_product_name.value,
            quantity=quantity.value
        )

        self.session.add(model)
        self.session.commit()


    def save_inventory_loss(
        self,
        inventory_loss: DomainInventoryLoss,
        product: DomainProduct
    ) -> None:

        model = InventoryLossModel(
            inventorylossid=inventory_loss.id.as_string(),
            productnameid=inventory_loss.product_name.value,
            quantity=inventory_loss.quantity.value,
            reason=inventory_loss.reason,
            registrationdate=inventory_loss.registration_date,
            observation=inventory_loss.observation
        )

        self.session.add(model)
        self.save(product)
        self.session.commit()


    def save_product_return(
        self,
        product_return: DomainProductReturn,
        product: DomainProduct
    ) -> None:

        if product_return.sale_detail_id is not None:
            model = ProductReturnModel(
                productreturnid=product_return.id.as_string(),
                saledetailid=product_return.sale_detail_id,
                quantity=product_return.quantity.value,
                reason=product_return.reason,
                registrationdate=product_return.registration_date
            )
            self.session.add(model)

        self.save(product)
        self.session.commit()


    def exists_by_id(
        self,
        id: ProductId
    ) -> bool:

        return (
            self.session.query(ProductModel)
            .filter(
                ProductModel.productnameid == id.get_value()
            )
            .first()
            is not None
        )


    def exists_by_bar_code(
        self,
        bar_code: BarCode
    ) -> bool:

        return (
            self.session.query(ProductModel)
            .filter(
                ProductModel.barcode == bar_code.value
            )
            .first()
            is not None
        )


    def find_by_id(
        self,
        id: ProductId
    ) -> Optional[DomainProduct]:

        model = (
            self.session.query(ProductModel)
            .filter(
                ProductModel.productnameid == id.get_value()
            )
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)


    def find_by_bar_code(
        self,
        bar_code: BarCode
    ) -> Optional[DomainProduct]:

        model = (
            self.session.query(ProductModel)
            .filter(
                ProductModel.barcode == bar_code.value
            )
            .first()
        )

        if model is None:
            return None

        return self._to_domain(model)


    def find_all_products(
        self
    ) -> List[DomainProduct]:

        products = (
            self.session
            .query(ProductModel)
            .all()
        )

        return [
            self._to_domain(product)
            for product in products
        ]


    def find_all_entries_by_product_id(
        self,
        id: ProductId
    ) -> List[DomainStockEntry]:

        entries = (
            self.session.query(StockEntryModel)
            .filter(
                StockEntryModel.productnameid == id.get_value()
            )
            .all()
        )

        return [
            self._stock_entry_to_domain(entry)
            for entry in entries
        ]


    def find_all_by_ids(
        self,
        product_ids: Set[ProductId]
    ) -> Set[DomainProduct]:

        ids = [
            product_id.get_value()
            for product_id in product_ids
        ]

        products = (
            self.session.query(ProductModel)
            .filter(
                ProductModel.productnameid.in_(ids)
            )
            .all()
        )

        return {
            self._to_domain(product)
            for product in products
        }


    def _to_domain(
        self,
        model: ProductModel
    ) -> DomainProduct:

        return DomainProduct.restore(
            product_name=model.productnameid,
            gain_strategy=model.gainstrategy,
            gain_amount=model.gainamount,
            reorder_level=model.reorderlevel,
            bar_code=model.barcode,
            sale_type=model.saletype,
            stock=model.stock,
            category=model.category,
            price=model.price,
            registration_date=model.registrationdate
        )


    def _stock_entry_to_domain(
        self,
        model: StockEntryModel
    ) -> DomainStockEntry:

        return DomainStockEntry.restore(
            stock_entry_id=model.stockentryid,
            product_name=model.productnameid,
            supplier_name=model.suppliernameid,
            unit_price=model.unitprice,
            quantity=model.quantity,
            registration_date=model.registrationdate,
            expiration_date=model.expirationdate
        )