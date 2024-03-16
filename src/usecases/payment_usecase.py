import uuid

from src.config.errors import ResourceNotFound

from src.entities.models.payment_entity import Payment
from src.interfaces.gateways.payment_gateway_interface import IPaymentGateway
from src.interfaces.use_cases.payment_usecase_interface import PaymentUseCaseInterface


class PaymentUseCase(PaymentUseCaseInterface):
    def __init__(self, payment_repo: IPaymentGateway) -> None:
        self._payment_repo = payment_repo

    def get_by_id(self, order_id: uuid.UUID):
        result = self._payment_repo.get_by_id(order_id)
        if not result:
            raise ResourceNotFound
        else:
            return result

    def get_all(self):
        return self._payment_repo.get_all()

    def confirm_payment(self, order_id: uuid.UUID, status: str) -> Payment:
        order = self._payment_repo.get_by_id(order_id)
        order.confirm_payment(status)
        updated_payment = self._payment_repo.update_payment(order_id, order)
        return updated_payment

    def create_payment(self, order_id: uuid.UUID) -> Payment:
        payment = Payment.create(order_id)
        self._payment_repo.create_payment(payment)
        return payment

    def remove_payment(self, order_id: uuid.UUID) -> None:
        self._payment_repo.remove_payment(order_id)
