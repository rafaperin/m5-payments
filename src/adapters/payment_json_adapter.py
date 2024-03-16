from typing import List

from src.entities.models.payment_entity import Payment
from src.utils.utils import camelize_dict


def payment_to_json(payment: Payment):
    payment_json = camelize_dict(payment.__dict__)
    return payment_json


def payment_list_to_json(payment_list: List[Payment]):
    return [camelize_dict(payment.__dict__) for payment in payment_list]


def qr_code_to_json(qr_code: str):
    return {"qrCode": qr_code}
