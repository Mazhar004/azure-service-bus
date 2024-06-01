import logging
import os
import time

from azure.servicebus import ServiceBusClient
from azure.servicebus.exceptions import OperationTimeoutError, ServiceBusError
from dotenv import load_dotenv

from utils import basic_logging

load_dotenv()
CONNECTION_STR = os.getenv('CONNECTION_STR_LISTEN')
TOPIC_NAME = os.getenv('TOPIC_NAME')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')

PULLING_FREQUENCY = 10  # In seconds
MAX_EMPTY_MESSAGES = 20  # Maximum consecutive empty message before stopping


class Subscriber:
    def __init__(self, connection_str: str, topic_name: str, subscription_name: str, pulling_frequency: int, max_empty_messages: int):
        self.connection_str = connection_str
        self.topic_name = topic_name
        self.subscription_name = subscription_name

        self.pulling_frequency = pulling_frequency
        self.max_empty_messages = max_empty_messages

        self.servicebus_client = ServiceBusClient.from_connection_string(conn_str=self.connection_str)

    def receive_messages(self) -> None:
        empty_message_count = 0

        with self.servicebus_client.get_subscription_receiver(self.topic_name, self.subscription_name) as receiver:
            while True:
                message_found = False
                try:
                    received_msgs = receiver.receive_messages(max_message_count=10,
                                                              max_wait_time=5)
                    if received_msgs:
                        for msg in received_msgs:
                            logger.info("Received Message from the Topic: %s", str(msg))

                            receiver.complete_message(msg)
                            message_found = True

                        empty_message_count = 0  # Reset counter on receiving messages
                    else:
                        empty_message_count += 1
                        logger.info("No messages received. Empty message count: %d",
                                    empty_message_count)

                        if empty_message_count >= self.max_empty_messages:
                            logger.error("Exceeded maximum empty message count. Stopping listener.")

                            raise Exception("Exceeded maximum empty message count. Stopping listener.")
                except (ServiceBusError, OperationTimeoutError) as Err:
                    logger.error("Failed to receive messages: %s", Err)
                    raise

                if not message_found:
                    # Sleep for the defined polling frequency before checking for messages again
                    logger.info("Sleeping for %d seconds before next poll.",
                                self.pulling_frequency)
                    time.sleep(self.pulling_frequency)


if __name__ == "__main__":
    logger = basic_logging.configure_logging()

    subscriber = Subscriber(connection_str=CONNECTION_STR,
                            topic_name=TOPIC_NAME,
                            subscription_name=SUBSCRIPTION_NAME,
                            pulling_frequency=PULLING_FREQUENCY,
                            max_empty_messages=MAX_EMPTY_MESSAGES)

    try:
        subscriber.receive_messages()
    except Exception as Err:
        logger.error("Listener stopped due to an error: %s", Err)
