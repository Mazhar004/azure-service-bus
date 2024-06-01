import argparse
import logging
import os
import time
from typing import Any

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import OperationTimeoutError, ServiceBusError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
CONNECTION_STR: str = os.getenv('CONNECTION_STR')
TOPIC_NAME: str = os.getenv('TOPIC_NAME')


class Publisher:
    def __init__(self, connection_str: str, topic_name: str, max_retries: int = 3, retry_delay: int = 5):
        self._connection_str = connection_str
        self.topic_name = topic_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.servicebus_client = ServiceBusClient.from_connection_string(conn_str=self._connection_str)

    def publish(self, data: Any) -> None:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Publish a message to a Service Bus topic.")
    parser.add_argument("--msg",
                        type=str,
                        required=True,
                        help="The message to publish.")

    args = parser.parse_args()

    publisher = Publisher(CONNECTION_STR, TOPIC_NAME)
    publisher.publish(args.msg)