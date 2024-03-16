from src.config.errors import DomainError


class PaymentError(DomainError):
    @classmethod
    def invalid_payment(cls) -> "PaymentError":
        return cls("Payment was unsuccessful!")
