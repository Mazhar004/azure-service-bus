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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--msg",
                        type=str,
                        required=True,
                        help="The message to publish.")
    parser.add_argument("--pubsub",
                        action="store_true",
                        help="If set, publish the message. Otherwise, only log.")
    args = parser.parse_args()

