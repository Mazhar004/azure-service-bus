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

