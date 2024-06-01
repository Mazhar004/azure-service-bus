import argparse
import asyncio
import logging
import os
from typing import Optional

from azure.identity.aio import DefaultAzureCredential
from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus.exceptions import OperationTimeoutError, ServiceBusError
from dotenv import load_dotenv

from utils import azure_monitor

load_dotenv()
FULLY_QUALIFIED_NAMESPACE = os.getenv('FULLY_QUALIFIED_NAMESPACE')
TOPIC_NAME = os.getenv('TOPIC_NAME')


class Publisher:
    def __init__(self, fully_qualified_namespace: str, topic_name: str):
        self.fully_qualified_namespace = fully_qualified_namespace
        self.topic_name = topic_name
        self.credential = DefaultAzureCredential()

    async def publish(self, message_body: str) -> None:
        try:
            message = ServiceBusMessage(message_body)

            servicebus_client = ServiceBusClient(self.fully_qualified_namespace,
                                                 self.credential)

            sender = servicebus_client.get_topic_sender(topic_name=self.topic_name)

            await sender.send_messages(message)
            logger.info(f'Published a message "{message_body}" to the topic "{self.topic_name}"')

        except (ServiceBusError, OperationTimeoutError) as Err:
            logger.error(f"An error occurred: {Err}", exc_info=True)
            raise


if __name__ == "__main__":
    logger = azure_monitor.configure_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--msg",
                        type=str,
                        required=True,
                        help="The message to publish.")
    parser.add_argument("--pubsub",
                        action="store_true",
                        help="If set, publish the message. Otherwise, only log.")
    args = parser.parse_args()

    if args.msg:
        publisher = Publisher(fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
                              topic_name=TOPIC_NAME)

        if args.pubsub:
            asyncio.run(publisher.publish(args.msg))
        else:
            logger.info(f"Logging message: {args.msg}")
