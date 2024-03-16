import json

import httpx

from src.config.errors import RepositoryError
from src.controllers.payment_controller import PaymentController
from src.config.config import settings
from src.entities.models.payment_entity import PaymentStatus
from src.external.messaging_client import MessagingClient


class MercadoPagoAPI:
    @staticmethod
    async def create_order_on_mercado_pago(order: dict):
        user_id = settings.MERCADO_PAGO_USER_ID
        external_pos_id = settings.MERCADO_PAGO_EXTERNAL_POS_ID
        access_token = settings.MERCADO_PAGO_ACCESS_TOKEN
        webhook_base_url = settings.WEBHOOK_BASE_URL

        mercado_pago_api_url = f"https://api.mercadopago.com/instore/orders/qr/seller/collectors/{user_id}/pos/{external_pos_id}/qrs"

        items = []
        for item in order["orderItems"]:
            product_id = item["productId"]

            headers = {
                #     "Authorization": f"Bearer {access_token}",
            }

            r = httpx.get(f"{settings.PRODUCTS_SERVICE}/products/id/{product_id}", headers=headers)
            json_response = json.loads(r.content)
            product = json_response["result"]

            order_item = {
                "sku_number": str(product["productId"]),
                "category": product["category"],
                "title": product["name"],
                "description": product["description"],
                "unit_price": float(product["price"]),
                "quantity": item["productQuantity"],
                "unit_measure": "unit",
                "total_amount": float(product["price"] * item["productQuantity"])
            }
            items.append(order_item)

        headers = {
            "Authorization": f"Bearer {access_token}",
        }

        params = {
            "external_reference": str(order["orderId"]),
            "total_amount": float(order["orderTotal"]),
            "items": items,
            "title": str(order["orderId"]),
            "description": f"Pedido {order['orderId']}",
            "notification_url": f"{webhook_base_url}/webhook"
        }

        r = httpx.post(mercado_pago_api_url, headers=headers, json=params)
        json_response = json.loads(r.content)

        return json_response["qr_data"]

    @staticmethod
    async def check_payment_approval(json_req: dict, params: list):
        if params[1] == 'merchant_order':
            url = json_req["resource"]
            headers = {
                "Authorization": f"Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}"}
            r = httpx.get(url, headers=headers)

            result = json.loads(r.content)
            if result["status"] == "closed":
                order_id = result["external_reference"]
                payment_status = result["payments"][0]["status"]

                try:
                    await PaymentController.confirm_payment(order_id, payment_status)

                    message = {"order_id": order_id,
                               "payment_status": PaymentStatus.CONFIRMED}

                    MessagingClient().send(settings.PAYMENT_CONFIRMATION_TOPIC, message)
                except Exception:
                    raise RepositoryError.get_operation_failed()
