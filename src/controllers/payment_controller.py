import uuid

from fastapi import APIRouter

from src.adapters.payment_json_adapter import payment_list_to_json, payment_to_json
from src.config.errors import RepositoryError, ResourceNotFound
from src.entities.schemas.payment_dto import CreatePaymentDTO
from src.gateways.postgres_gateways.payment_gateway import PostgresDBPaymentRepository
from src.usecases.payment_usecase import PaymentUseCase

router = APIRouter()


class PaymentController:
    @staticmethod
    async def confirm_payment(
        order_id: uuid.UUID,
        status: str
    ) -> dict:
        payment_gateway = PostgresDBPaymentRepository()

        try:
            payment = PaymentUseCase(payment_gateway).confirm_payment(order_id, status)
            result = payment_to_json(payment)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": result}

    @staticmethod
    async def get_all_payments() -> dict:
        payment_gateway = PostgresDBPaymentRepository()

        try:
            all_payments = PaymentUseCase(payment_gateway).get_all()
            result = payment_list_to_json(all_payments)
        except Exception as e:
            print(e)
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    async def get_payment_by_id(
        payment_id: uuid.UUID
    ) -> dict:
        payment_gateway = PostgresDBPaymentRepository()

        try:
            payment = PaymentUseCase(payment_gateway).get_by_id(payment_id)
            result = payment_to_json(payment)
        except ResourceNotFound:
            raise ResourceNotFound.get_operation_failed(f"No payment with id: {payment_id}")
        except Exception:
            raise RepositoryError.get_operation_failed()

        return result

    @staticmethod
    def create_payment(
        request: CreatePaymentDTO
    ) -> dict:
        payment_gateway = PostgresDBPaymentRepository()

        try:
            payment = PaymentUseCase(payment_gateway).create_payment(request.order_id)
            result = payment_to_json(payment)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return result

    @staticmethod
    async def remove_payment(
        payment_id: uuid.UUID
    ) -> dict:
        payment_gateway = PostgresDBPaymentRepository()

        try:
            PaymentUseCase(payment_gateway).remove_payment(payment_id)
        except Exception:
            raise RepositoryError.save_operation_failed()

        return {"result": "Payment removed successfully"}
