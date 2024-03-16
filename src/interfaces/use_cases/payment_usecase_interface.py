import uuid
from abc import ABC

from src.entities.models.payment_entity import Payment
from src.interfaces.gateways.payment_gateway_interface import IPaymentGateway


class PaymentUseCaseInterface(ABC):
    def __init__(self, payment_repo: IPaymentGateway) -> None:
        raise NotImplementedError

    def get_by_id(self, order_id: uuid.UUID):
        pass

    def get_all(self):
        pass

    def create_payment(self, order_id: uuid.UUID) -> Payment:
        pass

    def confirm_payment(self, order_id: uuid.UUID, status: str) -> Payment:
        pass

    def remove_payment(self, order_id: uuid.UUID) -> Payment:
        pass
