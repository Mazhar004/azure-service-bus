import asyncio
import logging
import os
from datetime import datetime
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus import ServiceBusReceivedMessage
from azure.servicebus.aio import ServiceBusClient
from dotenv import load_dotenv

from utils import azure_monitor

load_dotenv()
FULLY_QUALIFIED_NAMESPACE = os.getenv('FULLY_QUALIFIED_NAMESPACE')
TOPIC_NAME = os.getenv('TOPIC_NAME')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')


PULLING_FREQUENCY_SECONDS = 5  # In seconds
EMPTY_MESSAGES_THRESHOLD = 10  # Number of empty messages before exiting


