from src.entities.schemas.payment_dto import CreatePaymentDTO


def message_to_new_order_dto(message: dict):
    return CreatePaymentDTO(order_id=message["order_id"])
