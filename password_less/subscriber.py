import asyncio
import logging
import os

from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from dotenv import load_dotenv

from utils import azure_monitor

load_dotenv()
FULLY_QUALIFIED_NAMESPACE = os.getenv('FULLY_QUALIFIED_NAMESPACE')
TOPIC_NAME = os.getenv('TOPIC_NAME')
SUBSCRIPTION_NAME = os.getenv('SUBSCRIPTION_NAME')

PULLING_FREQUENCY_SECONDS = 5  # In seconds
EMPTY_MESSAGES_THRESHOLD = 10  # Number of empty messages before exiting


class Subscriber:
    def __init__(self):
        self.credential = DefaultAzureCredential()

    async def run(self) -> None:
        # create a Service Bus client using the credential
        async with ServiceBusClient(fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
                                    credential=self.credential,
                                    logging_enable=True) as servicebus_client:

            # get the Subscription Receiver object for the subscription
            receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME,
                                                                   subscription_name=SUBSCRIPTION_NAME,
                                                                   max_wait_time=5)
            async with receiver:
                empty_messages_count = 0

                while True:
                    received_msgs = await receiver.receive_messages(max_wait_time=5,
                                                                    max_message_count=20)
                    if not received_msgs:
                        empty_messages_count += 1
                        logger.info(f'No messages received, empty count: {empty_messages_count}')
                        if empty_messages_count >= EMPTY_MESSAGES_THRESHOLD:
                            logger.info(f'Empty messages count threshold reached, exiting...')
                            break
                    else:
                        empty_messages_count = 0

                        for msg in received_msgs:
                            logger.info(
                                "Received Message from the Topic: %s", str(msg))
                            await receiver.complete_message(msg)

                    if not received_msgs:
                        logger.info(f'No messages found, sleeping... for {PULLING_FREQUENCY_SECONDS} seconds')
                        await asyncio.sleep(PULLING_FREQUENCY_SECONDS)

            await self.credential.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('azure').setLevel(logging.WARNING)
    main()
