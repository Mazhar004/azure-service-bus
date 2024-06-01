import logging
import os
import time

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import OperationTimeoutError, ServiceBusError
from dotenv import load_dotenv

load_dotenv()
CONNECTION_STR = os.getenv('CONNECTION_STR_LISTEN')
TOPIC_NAME = os.getenv('TOPIC_NAME')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')


PULLING_FREQUENCY = 10  # in seconds

# Maximum number of consecutive empty message checks before stopping
MAX_EMPTY_MESSAGES = 180

