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

with servicebus_client.get_topic_sender(topic_name) as sender:
    for attempt in range(max_retries):
        try:
            message = ServiceBusMessage(data)
            sender.send_messages(message)
            logger.info("Message published successfully on attempt %d", attempt + 1)
            break
        except (ServiceBusError, OperationTimeoutError) as e:
            logger.warning("Attempt %d: Failed to publish message: %s", attempt + 1, e)
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                logger.error("Exceeded max retries. Failed to publish message after %d attempts.", max_retries)
                raise e


print("Message published.")
