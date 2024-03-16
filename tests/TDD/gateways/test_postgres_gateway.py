import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.entities.models.payment_entity import Payment
from src.interfaces.gateways.payment_gateway_interface import IPaymentGateway
from tests.utils.payment_helper import PaymentHelper


class MockRepository(IPaymentGateway):

    def get_by_id(self, order_id: uuid.UUID) -> Payment:
        pass

    def get_all(self) -> List[Payment]:
        pass

    def create_payment(self, payment_in: Payment) -> Payment:
        pass

    def update_payment(self, order_id: uuid.UUID, payment_in: Payment) -> Payment:
        pass

    def remove_payment(self, order_id: uuid.UUID) -> None:
        pass


payment_repo = MockRepository()


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_payment():
    return PaymentHelper.generate_payment_entity()


@pytest.fixture
def generate_multiple_payments():
    return PaymentHelper.generate_multiple_payment_entities()


def test_should_allow_register_payment(generate_new_payment, unstub):
    payment = generate_new_payment

    when(payment_repo).create_payment(ANY(Payment)).thenReturn(payment)

    created_payment = payment_repo.create_payment(payment)

    verify(payment_repo, times=1).create_payment(payment)

    assert type(created_payment) == Payment
    assert created_payment is not None
    assert created_payment == payment
    assert payment.order_id == created_payment.order_id
    assert payment.creation_date == created_payment.creation_date
    assert payment.payment_status == created_payment.payment_status


def test_should_allow_retrieve_payment_by_id(generate_new_payment, unstub):
    payment = generate_new_payment
    order_id = payment.order_id

    when(payment_repo).get_by_id(ANY(uuid.UUID)).thenReturn(payment)

    retrieved_payment = payment_repo.get_by_id(order_id)

    verify(payment_repo, times=1).get_by_id(order_id)

    assert payment.order_id == retrieved_payment.order_id
    assert payment.creation_date == retrieved_payment.creation_date
    assert payment.payment_status == retrieved_payment.payment_status


def test_should_allow_update_payment(generate_new_payment, unstub):
    payment = generate_new_payment
    order_id = payment.order_id

    updated_payment = generate_new_payment
    payment.creation_date = updated_payment.creation_date
    payment.payment_status = updated_payment.payment_status

    when(payment_repo).update_payment(ANY(uuid.UUID), ANY(Payment)).thenReturn(payment)

    created_payment = payment_repo.update_payment(order_id, payment)

    verify(payment_repo, times=1).update_payment(order_id, payment)

    assert type(created_payment) == Payment
    assert created_payment is not None
    assert created_payment == payment
    assert payment.order_id == created_payment.order_id
    assert payment.creation_date == created_payment.creation_date
    assert payment.payment_status == created_payment.payment_status


def test_should_allow_list_payments(generate_multiple_payments, unstub):
    payments_list = generate_multiple_payments

    when(payment_repo).get_all().thenReturn(payments_list)

    result = payment_repo.get_all()

    verify(payment_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(payments_list)
    for payment in payments_list:
        assert payment in result


def test_should_allow_remove_payment(unstub):
    payment_id = uuid.uuid4()

    when(payment_repo).remove_payment(ANY(uuid.UUID)).thenReturn()

    payment_repo.remove_payment(payment_id)

    verify(payment_repo, times=1).remove_payment(payment_id)
