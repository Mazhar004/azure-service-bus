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


def receive_messages():
    servicebus_client = ServiceBusClient.from_connection_string(
        conn_str=CONNECTION_STR)
    empty_message_count = 0

    with servicebus_client.get_subscription_receiver(TOPIC_NAME, SUBSCRIPTION_NAME) as receiver:
        while True:
            message_found = False
            try:
                received_msgs = receiver.receive_messages(max_message_count=10,
                                                          max_wait_time=5)
                if received_msgs:
                    for count, msg in enumerate(received_msgs):
                        logger.info(
                            "Received Message from the Topic: %s", str(msg))
                        print(msg)
                        receiver.complete_message(msg)
                        message_found = True

                    empty_message_count = 0  # Reset counter on receiving messages
                else:
                    empty_message_count += 1
                    logger.info(
                        "No messages received. Empty message count: %d", empty_message_count)
                    if empty_message_count >= MAX_EMPTY_MESSAGES:
                        logger.error(
                            "Exceeded maximum empty message count. Stopping listener.")
                        raise Exception(
                            "Exceeded maximum empty message count. Stopping listener.")
            except (ServiceBusError, OperationTimeoutError) as e:
                logger.error("Failed to receive messages: %s", e)
                raise

            if not message_found:
                # Sleep for the defined polling frequency before checking for messages again
                logger.info(
                    "Sleeping for %d seconds before next poll.", PULLING_FREQUENCY)
                time.sleep(PULLING_FREQUENCY)

