import uuid
from typing import List

import pytest
from mockito import when, verify, ANY

from src.config.errors import ResourceNotFound
from src.entities.models.payment_entity import Payment, PaymentStatus
from src.interfaces.gateways.payment_gateway_interface import IPaymentGateway
from src.interfaces.use_cases.payment_usecase_interface import PaymentUseCaseInterface
from src.usecases.payment_usecase import PaymentUseCase
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


class MockUsecase(PaymentUseCaseInterface):
    pass


payment_repo = MockRepository()
payment_usecase = PaymentUseCase(payment_repo)


@pytest.fixture
def unstub():
    from mockito import unstub
    yield
    unstub()


@pytest.fixture
def generate_new_payment():
    return PaymentHelper.generate_payment_entity()


@pytest.fixture
def generate_new_payment_dto():
    return PaymentHelper.generate_payment_request()


@pytest.fixture
def generate_multiple_payments():
    return PaymentHelper.generate_multiple_payment_entities()


def test_should_allow_register_payment(generate_new_payment_dto, unstub):
    payment_dto = generate_new_payment_dto
    payment_entity = Payment.create(
        order_id=payment_dto.order_id,
    )

    when(payment_repo).create_payment(ANY(Payment)).thenReturn(payment_entity)

    created_payment = payment_usecase.create_payment(payment_dto.order_id)

    assert created_payment is not None
    assert payment_dto.order_id == created_payment.order_id
    assert payment_entity.payment_status == created_payment.payment_status


def test_should_allow_retrieve_payment_by_id(generate_new_payment_dto, unstub):
    payment = generate_new_payment_dto
    payment_id = uuid.uuid4()

    when(payment_repo).get_by_id(ANY(uuid.UUID)).thenReturn(payment)

    retrieved_payment = payment_usecase.get_by_id(payment_id)

    verify(payment_repo, times=1).get_by_id(payment_id)

    assert retrieved_payment is not None
    assert payment.order_id == retrieved_payment.order_id


def test_should_raise_exception_invalid_id(unstub):
    payment_id = uuid.uuid4()

    when(payment_repo).get_by_id(ANY(uuid.UUID)).thenReturn()

    try:
        payment_usecase.get_by_id(payment_id)
        assert False
    except ResourceNotFound:
        assert True

    verify(payment_repo, times=1).get_by_id(payment_id)


def test_should_allow_update_payment(generate_new_payment, generate_new_payment_dto, unstub):
    old_payment = generate_new_payment
    old_payment_id = old_payment.order_id
    new_payment_status = "approved"

    old_payment.payment_status = new_payment_status

    when(payment_repo).get_by_id(ANY(uuid.UUID)).thenReturn(old_payment)
    when(payment_repo).update_payment(ANY(uuid.UUID), ANY(Payment)).thenReturn(old_payment)

    updated_payment = payment_usecase.confirm_payment(old_payment_id, new_payment_status)

    assert updated_payment is not None
    assert updated_payment.order_id == old_payment.order_id
    assert updated_payment.payment_status == old_payment.payment_status


def test_should_allow_list_payments(generate_multiple_payments, unstub):
    payments_list = generate_multiple_payments

    when(payment_repo).get_all().thenReturn(payments_list)

    result = payment_usecase.get_all()

    verify(payment_repo, times=1).get_all()

    assert type(result) == list
    assert len(result) == len(payments_list)
    for payment in payments_list:
        assert payment in result


def test_should_allow_list_empty_payments(generate_multiple_payments, unstub):
    when(payment_repo).get_all().thenReturn(list())

    result = payment_usecase.get_all()

    assert result == list()
    verify(payment_repo, times=1).get_all()


def test_should_allow_remove_payment(unstub):
    payment_id = uuid.uuid4()

    when(payment_repo).remove_payment(ANY(uuid.UUID)).thenReturn()

    payment_usecase.remove_payment(payment_id)

    verify(payment_repo, times=1).remove_payment(payment_id)
