from domain.valueObject.PhoneNumber import PhoneNumber
from domain.entities.customer.CustomerId import CustomerId
from domain.repositories.CustomerRepository import CustomerRepository
from typing import Optional, List

from sqlalchemy.orm import Session

from domain.entities.customer.Customer import Customer as DomainCustomer
from infrastructure.persistence.models import Customer as CustomerModel


class SqlAlchemyCustomerRepository(CustomerRepository):

    def __init__(self, session: Session):
        self.session = session


    def save(
        self,
        customer: DomainCustomer
    ) -> None:

        customer_model = CustomerModel(
            customernameid=customer.id.as_string(),
            registrationdate=customer.registration_date,
            phonenumber=(
                customer.phone_number.value
                if customer.phone_number
                else None
            )
        )

        self.session.merge(customer_model)
        self.session.commit()


    def exists_by_id(
        self,
        id: CustomerId
    ) -> bool:

        return (
            self.session.query(CustomerModel)
            .filter(
                CustomerModel.customernameid == id.as_string()
            )
            .first()
            is not None
        )


    def exists_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> bool:

        return (
            self.session.query(CustomerModel)
            .filter(
                CustomerModel.phonenumber == phone_number.value
            )
            .first()
            is not None
        )


    def find_by_id(
        self,
        id: CustomerId
    ) -> Optional[DomainCustomer]:

        customer = (
            self.session.query(CustomerModel)
            .filter(
                CustomerModel.customernameid == id.as_string()
            )
            .first()
        )

        if not customer:
            return None

        return self._to_domain(customer)


    def find_by_phone_number(
        self,
        phone_number: PhoneNumber
    ) -> Optional[DomainCustomer]:

        customer = (
            self.session.query(CustomerModel)
            .filter(
                CustomerModel.phonenumber == phone_number.value
            )
            .first()
        )

        if not customer:
            return None

        return self._to_domain(customer)


    def find_all(
        self
    ) -> List[DomainCustomer]:

        customers = (
            self.session
            .query(CustomerModel)
            .all()
        )

        return [
            self._to_domain(customer)
            for customer in customers
        ]


    def _to_domain(
        self,
        model: CustomerModel
    ) -> DomainCustomer:

        return DomainCustomer.restore(
            customer_name=model.customernameid.strip() if model.customernameid else model.customernameid,
            registration_date=model.registrationdate,
            phone_number=model.phonenumber.strip() if model.phonenumber else model.phonenumber
        )