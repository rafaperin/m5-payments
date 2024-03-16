import datetime
import uuid
from typing import List

from src.utils.utils import CamelModel


class PaymentDTO(CamelModel):
    order_id: uuid.UUID
    creation_date: datetime.datetime
    payment_status: str

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
                "creation_date": "2024-01-01T00:05:23",
                "payment_status": "Confirmado"
            }
        }


class GenerateQrCodeDTO(CamelModel):
    qr_code: str

    class Config:
        schema_extra = {
            "example": {
                "qr_code": "00020101021243650016COM.MERCADOLIBRE020130636bb094b54-a1c0-4996-9a13-fd2a98e68b145204000053039865802BR5913Loja Tech 0016009SAO PAULO62070503***6304FF0A",
            }
        }


class CreatePaymentDTO(CamelModel):
    order_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
            }
        }


class RemovePaymentDTO(CamelModel):
    order_id: uuid.UUID

    class Config:
        schema_extra = {
            "example": {
                "order_id": "00000000-0000-0000-0000-000000000000",
            }
        }


class PaymentDTOResponse(CamelModel):
    result: PaymentDTO


class PaymentDTOListResponse(CamelModel):
    result: List[PaymentDTO]


class QrCodeResponse(CamelModel):
    result: GenerateQrCodeDTO
