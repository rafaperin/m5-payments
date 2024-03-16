import uuid
from abc import ABC, abstractmethod
from typing import List

from src.entities.models.payment_entity import Payment


class IPaymentGateway(ABC):
    @abstractmethod
    def get_by_id(self, order_id: uuid.UUID) -> Payment:
        pass

    @abstractmethod
    def get_all(self) -> List[Payment]:
        pass

    @abstractmethod
    def create_payment(self, payment_in: Payment) -> Payment:
        pass

    @abstractmethod
    def update_payment(self, order_id: uuid.UUID, payment_in: Payment) -> Payment:
        pass

    @abstractmethod
    def remove_payment(self, order_id: uuid.UUID) -> None:
        pass
