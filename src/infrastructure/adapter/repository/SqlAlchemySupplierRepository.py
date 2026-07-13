from typing import Optional, List

from sqlalchemy.orm import Session

from domain.entities.supplier.Supplier import Supplier as DomainSupplier
from domain.entities.supplier.SupplierId import SupplierId

from domain.repositories.SupplierRepository import SupplierRepository

from domain.valueObject.PhoneNumber import PhoneNumber
from domain.valueObject.RUC import RUC

from infrastructure.persistence.models import Supplier as SupplierModel


class SqlAlchemySupplierRepository(SupplierRepository):

    def __init__(
        self,
        session: Session
    ):
        self.session = session


    def save(
        self,
        supplier: DomainSupplier
    ) -> None:

        model = SupplierModel(
            suppliernameid=supplier.supplier_name.value,
            registrationdate=supplier.registration_date,
            ruc=(
                supplier.ruc.value
                if supplier.ruc is not None
                else None
            ),
            phonenumber=(
                supplier.phone_number.value
                if supplier.phone_number is not None
                else None
            )
        )

        self.session.merge(model)
        self.session.commit()



    def exists_by_id(
        self,
        id: SupplierId
    ) -> bool:

        return (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.suppliernameid == id.get_value()
            )
            .first()
            is not None
        )



    def exists_by_ruc(
        self,
        ruc: RUC
    ) -> bool:

        return (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.ruc == ruc.value
            )
            .first()
            is not None
        )



    def exists_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> bool:

        return (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.phonenumber == phone_number.value
            )
            .first()
            is not None
        )



    def find_all(
        self
    ) -> List[DomainSupplier]:

        suppliers = (
            self.session
            .query(SupplierModel)
            .all()
        )

        return [
            self._to_domain(supplier)
            for supplier in suppliers
        ]



    def find_by_id(
        self,
        id: SupplierId
    ) -> Optional[DomainSupplier]:

        supplier = (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.suppliernameid == id.get_value()
            )
            .first()
        )

        if supplier is None:
            return None

        return self._to_domain(supplier)



    def find_by_ruc(
        self,
        ruc: RUC
    ) -> Optional[DomainSupplier]:

        supplier = (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.ruc == ruc.value
            )
            .first()
        )

        if supplier is None:
            return None

        return self._to_domain(supplier)



    def find_by_phone(
        self,
        phone_number: PhoneNumber
    ) -> Optional[DomainSupplier]:

        supplier = (
            self.session.query(SupplierModel)
            .filter(
                SupplierModel.phonenumber == phone_number.value
            )
            .first()
        )

        if supplier is None:
            return None

        return self._to_domain(supplier)



    def _to_domain(
        self,
        model: SupplierModel
    ) -> DomainSupplier:

        return DomainSupplier.restore(
            supplier_name=model.suppliernameid.strip() if model.suppliernameid else model.suppliernameid,
            ruc=model.ruc.strip() if model.ruc else model.ruc,
            phone_number=model.phonenumber.strip() if model.phonenumber else model.phonenumber,
            registration_date=model.registrationdate
        )