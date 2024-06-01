from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError, OperationTimeoutError

import logging
from dotenv import load_dotenv
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
connection_str = os.getenv('CONNECTION_STR')
topic_name = os.getenv('TOPIC_NAME')
max_retries = 3

servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)

retry_delay = 5

