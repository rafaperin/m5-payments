import json
import uuid

import httpx
from fastapi import APIRouter, Request, status

from src.adapters.payment_json_adapter import qr_code_to_json
from src.api.errors.api_errors import APIErrorMessage
from src.config.config import settings
from src.config.errors import RepositoryError, ResourceNotFound
from src.controllers.payment_controller import PaymentController
from src.entities.schemas.payment_dto import CreatePaymentDTO, PaymentDTOResponse, PaymentDTOListResponse, \
    QrCodeResponse
from src.external.mercado_pago_api import MercadoPagoAPI
from src.external.messaging_client import MessagingClient

router = APIRouter(tags=["Payment"])


@router.post("/webhook", tags=["Webhook"])
async def payment_webhook(request: Request):
    json_req = await request.json()
    params = list(request.query_params.values())
    print(json_req)
    print(params)

    await MercadoPagoAPI.check_payment_approval(json_req, params)


@router.get(
    "/payments",
    response_model=PaymentDTOListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_all_payments() -> dict:
    try:
        result = await PaymentController.get_all_payments()
    except Exception as e:
        print(e)
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.post(
    "/payments/mercado-pago",
    response_model=QrCodeResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_order_on_mercado_pago(order: CreatePaymentDTO) -> dict:
    try:

        headers = {
            # "Authorization": f"Bearer {access_token}",
        }

        r = httpx.get(f"{settings.ORDERS_SERVICE}/orders/id/{order.order_id}", headers=headers)
        json_response = json.loads(r.content)
        order = json_response["result"]

        qr_code = await MercadoPagoAPI.create_order_on_mercado_pago(order)
        result = qr_code_to_json(qr_code)
    except Exception:
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.get(
    "/payments/id/{order_id}",
    response_model=PaymentDTOResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def get_payment_by_id(
    order_id: uuid.UUID
) -> dict:
    try:
        result = await PaymentController.get_payment_by_id(order_id)
    except ResourceNotFound:
        raise ResourceNotFound.get_operation_failed(f"No payment with order id: {order_id}")
    except Exception:
        raise RepositoryError.get_operation_failed()

    return {"result": result}


@router.post(
    "/payments",
    response_model=PaymentDTOResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def create_payment(
    request: CreatePaymentDTO
) -> dict:
    try:
        result = PaymentController.create_payment(request)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": result}


@router.delete(
    "/payments/{order_id}",
    status_code=status.HTTP_200_OK,
    responses={400: {"model": APIErrorMessage},
               404: {"model": APIErrorMessage},
               500: {"model": APIErrorMessage}}
)
async def remove_payment(
    order_id: uuid.UUID
) -> dict:
    try:
        await PaymentController.remove_payment(order_id)
    except Exception:
        raise RepositoryError.save_operation_failed()

    return {"result": "Payment removed successfully"}
