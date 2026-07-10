from domain.repositories.ProductRepository import ProductRepository
from domain.entities.sale.Sale import Sale as DomainSale
from domain.entities.sale.SaleId import SaleId
from domain.entities.sale.SaleDetailId import SaleDetailId
from domain.entities.sale.PayId import PayId

from domain.entities.customer.CustomerId import CustomerId
from domain.entities.product.Product import Product as DomainProduct

from domain.entities.sale.DTO import SaleDetailDTO
from domain.entities.sale.DTO import PayDTO

from domain.repositories.SaleRepository import SaleRepository

from infrastructure.persistence.models import (
    Sale as SaleModel,
    Saledetail as SaleDetailModel,
    Pay as PayModel
)

from sqlalchemy.orm import Session

from typing import Optional, List, Set


class SqlAlchemySaleRepository(SaleRepository):

    def __init__(
        self,
        product_repository: ProductRepository,
        session: Session
    ):
        self.product_repository = product_repository
        self.session = session


    def save(
        self,
        sale: DomainSale,
        products: Set[DomainProduct]
    ) -> None:

        sale_model = SaleModel(
            saleid=sale.id.as_string(),
            customernameid=sale.customer_id.value,
            registrationdate=sale.registration_date
        )

        self.session.add(sale_model)


        for detail in sale.get_sale_details():

            detail_model = SaleDetailModel(
                saledetailid=detail.sale_detail_id,
                saleid=sale.id.as_string(),
                productnameid=detail.product_id,
                quantity=detail.quantity,
                unitprice=detail.unit_price
            )

            self.session.add(detail_model)


        for pay in sale.get_pays():

            pay_model = PayModel(
                payid=pay.pay_id,
                saleid=sale.id.as_string(),
                amount=pay.amount,
                paymentmethod=pay.payment_method,
                registrationdate=pay.registration_date
            )

            self.session.add(pay_model)

        for product in products:
            self.product_repository.save(product)


        self.session.commit()


    def find_by_id(
        self,
        id: SaleId
    ) -> Optional[DomainSale]:

        model = (
            self.session.query(SaleModel)
            .filter(
                SaleModel.saleid == id.as_string()
            )
            .first()
        )

        if model is None:
            return None


        return self._to_domain(model)



    def find_by_customer_id(
        self,
        customer_id: CustomerId
    ) -> List[DomainSale]:

        sales = (
            self.session.query(SaleModel)
            .filter(
                SaleModel.customernameid == customer_id.get_value()
            )
            .all()
        )

        return [
            self._to_domain(sale)
            for sale in sales
        ]



    def find_all(
        self
    ) -> List[DomainSale]:

        sales = (
            self.session.query(SaleModel)
            .all()
        )

        return [
            self._to_domain(sale)
            for sale in sales
        ]



    def find_sale_details_by_id(
        self,
        id: SaleDetailId
    ) -> List[SaleDetailDTO]:

        details = (
            self.session.query(SaleDetailModel)
            .filter(
                SaleDetailModel.saledetailid == id.as_string()
            )
            .all()
        )


        return [
            SaleDetailDTO(
                detail.saledetailid,
                detail.productnameid,
                detail.quantity,
                detail.unitprice
            )
            for detail in details
        ]



    def find_pays_by_id(
        self,
        id: PayId
    ) -> List[PayDTO]:

        pays = (
            self.session.query(PayModel)
            .filter(
                PayModel.payid == str(id)
            )
            .all()
        )


        return [
            PayDTO(
                pay.payid,
                pay.amount,
                pay.paymentmethod,
                pay.registrationdate
            )
            for pay in pays
        ]



    def update_payments(
        self,
        sale: DomainSale
    ) -> None:

        for pay in sale.get_pays():

            model = PayModel(
                payid=pay.pay_id,
                saleid=sale.id.as_string(),
                amount=pay.amount,
                paymentmethod=pay.payment_method,
                registrationdate=pay.registration_date
            )

            self.session.merge(model)


        self.session.commit()



    def _to_domain(
        self,
        model: SaleModel
    ) -> DomainSale:

        details = (
            self.session.query(SaleDetailModel)
            .filter(
                SaleDetailModel.saleid == model.saleid
            )
            .all()
        )


        pays = (
            self.session.query(PayModel)
            .filter(
                PayModel.saleid == model.saleid
            )
            .all()
        )


        return DomainSale.restore(
            sale_id=model.saleid,
            customer_name_id=model.customernameid,
            registration_date=model.registrationdate,
            sale_details=details,
            pays=pays
        )