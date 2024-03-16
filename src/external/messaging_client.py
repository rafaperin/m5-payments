import json

import boto3
from botocore.config import Config

my_config = Config(
    region_name='us-east-1'
)

sqs_client = boto3.client('sqs', config=my_config)
sns_client = boto3.client('sns', config=my_config)


class MessagingClient:
    @staticmethod
    def receive(queue: str):
        response = sqs_client.receive_message(
            QueueUrl=queue,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=5
        )

        if 'Messages' in response:
            message = response['Messages'][0]
            return message
        else:
            return None

    @staticmethod
    def send(topic: str, message: dict):
        sns_client.publish(
            TopicArn=topic,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
