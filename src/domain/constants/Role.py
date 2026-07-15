from domain.constants.Permission import Permission
from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    VENDEDOR = "VENDEDOR"
    ALMACENISTA = "ALMACENISTA"

    @property
    def permissions(self) -> set[Permission]:
        match self:
            case Role.ADMIN:
                return set(Permission)

            case Role.VENDEDOR:
                return {
                    Permission.CUSTOMER_REGISTER,
                    Permission.CUSTOMER_UPDATE_PHONE_NUMBER,
                    Permission.CUSTOMER_FIND_BY_ID,
                    Permission.CUSTOMER_FIND_BY_PHONE_NUMBER,
                    Permission.CUSTOMER_GET_ALL,
                    Permission.PRODUCT_FIND_BY_ID,
                    Permission.PRODUCT_FIND_BY_BAR_CODE,
                    Permission.PRODUCT_FIND_ALL,
                    Permission.SALE_REGISTER,
                    Permission.SALE_ADD_PAYMENT,
                    Permission.SALE_FIND_BY_ID,
                    Permission.SALE_FIND_BY_CUSTOMER_ID,
                    Permission.SALE_FIND_ALL,
                }

            case Role.ALMACENISTA:
                return {
                    Permission.PRODUCT_REGISTER,
                    Permission.PRODUCT_REGISTER_STOCK_ENTRY,
                    Permission.PRODUCT_REGISTER_INVENTORY_LOSS,
                    Permission.PRODUCT_REGISTER_PRODUCT_RETURN,
                    Permission.PRODUCT_ASSOCIATE_UNIT_TO_BULK,
                    Permission.PRODUCT_FIND_BY_ID,
                    Permission.PRODUCT_FIND_BY_BAR_CODE,
                    Permission.PRODUCT_FIND_ALL,
                    Permission.SUPPLIER_REGISTER,
                    Permission.SUPPLIER_UPDATE_PHONE_NUMBER,
                    Permission.SUPPLIER_UPDATE_RUC,
                    Permission.SUPPLIER_FIND_ALL,
                    Permission.SUPPLIER_FIND_BY_ID,
                    Permission.SUPPLIER_FIND_BY_RUC,
                    Permission.SUPPLIER_FIND_BY_PHONE_NUMBER,
                }

    def has_permission(self, permission: Permission) -> bool:
        return permission in self.permissions

    def lacks_permission(self, permission: Permission) -> bool:
        return permission not in self.permissions