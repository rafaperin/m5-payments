import json
import threading
import time

from src.adapters.message_to_dto_adapter import message_to_new_order_dto
from src.config.config import settings
from src.controllers.payment_controller import PaymentController
from src.external.messaging_client import MessagingClient, sqs_client


class NewOrderListener(threading.Thread):
    def __init__(self):
        super().__init__()
        self.queue = settings.NEW_ORDER_QUEUE
        self.shutdown_flag = threading.Event()

    def run(self, *args, **kwargs):
        while not self.shutdown_flag.is_set():
            message = MessagingClient().receive(self.queue)
            if message is not None:
                try:
                    receipt_handle = message['ReceiptHandle']
                    message_body = json.loads(message["Body"])
                    content = json.loads(message_body["Message"])

                    request = message_to_new_order_dto(content)
                    PaymentController.create_payment(request)

                    sqs_client.delete_message(
                        QueueUrl=self.queue,
                        ReceiptHandle=receipt_handle
                    )
                    time.sleep(5)
                except Exception as e:
                    print(e)

            print("new order listener running")
