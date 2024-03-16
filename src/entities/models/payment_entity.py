import datetime
import uuid
from dataclasses import dataclass

from src.entities.errors.payment_error import PaymentError


class OrderStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"


class PaymentStatus:
    PENDING = "Pendente"
    CONFIRMED = "Confirmado"
    REFUSED = "Negado"


@dataclass
class Payment:
    order_id: uuid.UUID
    creation_date: datetime.datetime
    payment_status: str

    @classmethod
    def create(cls, order_id: uuid.UUID) -> "Payment":
        if not order_id:
            raise PaymentError("Order id is required")

        return cls(order_id, datetime.datetime.utcnow(), PaymentStatus.PENDING)

    def check_payment_status(self) -> None:
        if self.payment_status == PaymentStatus.PENDING:
            raise PaymentError("Order payment id pending!")
        if self.payment_status == PaymentStatus.REFUSED:
            raise PaymentError("Order payment was refused! Please contact your payment provider.")

    def confirm_payment(self, status: str) -> None:
        if status == "approved":
            self.payment_status = PaymentStatus.CONFIRMED
        else:
            raise PaymentError("Order not yet confirmed!")


def payment_factory(
    order_id: uuid.UUID,
    creation_date: datetime.datetime,
    payment_status: str
) -> Payment:
    return Payment(
        order_id=order_id,
        creation_date=creation_date,
        payment_status=payment_status
    )
