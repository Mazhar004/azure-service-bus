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

class Publisher:
    def __init__(self, servicebus_client, topic_name, max_retries=3, retry_delay=5):
        self.servicebus_client = servicebus_client
        self.topic_name = topic_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def publish(self, data):
        with self.servicebus_client.get_topic_sender(self.topic_name) as sender:
            for attempt in range(self.max_retries):
                try:
                    message = ServiceBusMessage(data)
                    sender.send_messages(message)
                    logger.info("Message published successfully on attempt %d", attempt + 1)
                    break
                except (ServiceBusError, OperationTimeoutError) as e:
                    logger.warning("Attempt %d: Failed to publish message: %s", attempt + 1, e)
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
                    else:
                        logger.error("Exceeded max retries. Failed to publish message after %d attempts.", self.max_retries)
                        raise e

        print("Message published.")


publisher = Publisher(servicebus_client, topic_name)
publisher.publish(data)