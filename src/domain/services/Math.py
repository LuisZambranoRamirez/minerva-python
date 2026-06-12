from decimal import Decimal


class Math:

    @staticmethod
    def is_integer(number: Decimal) -> bool:
        return number is not None and number == number.to_integral_value()

    @staticmethod
    def is_decimal(number: Decimal) -> bool:
        return number is not None and number != number.to_integral_value()

    @staticmethod
    def is_positive(number: Decimal) -> bool:
        return number is not None and number > 0

    @staticmethod
    def is_negative(number: Decimal) -> bool:
        return number is not None and number < 0
