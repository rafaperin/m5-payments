import uuid
from typing import List

from src.entities.models.payment_entity import Payment
from src.entities.schemas.payment_dto import CreatePaymentDTO


class PaymentHelper:

    @staticmethod
    def generate_payment_request() -> CreatePaymentDTO:
        return CreatePaymentDTO(
            order_id=uuid.uuid4()
        )

    @staticmethod
    def generate_multiple_payments() -> List[CreatePaymentDTO]:
        payments_list = []
        payment1 = CreatePaymentDTO(
            order_id=uuid.uuid4()
        )

        payment2 = CreatePaymentDTO(
            order_id=uuid.uuid4()
        )

        payments_list.append(payment1)
        payments_list.append(payment2)
        return payments_list

    @staticmethod
    def generate_payment_entity() -> Payment:
        return Payment.create(
            order_id=uuid.uuid4()
        )

    @staticmethod
    def generate_multiple_payment_entities() -> List[Payment]:
        payments_list = []
        payment1 = Payment.create(
            order_id=uuid.uuid4()
        )

        payment2 = Payment.create(
            order_id=uuid.uuid4()
        )
        payments_list.append(payment1)
        payments_list.append(payment2)
        return payments_list
