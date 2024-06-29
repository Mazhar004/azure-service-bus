import asyncio
import logging

from message import TopicMessageReceiverStrategy

from client import ServiceBusClientFactory
from utils import (ServiceBusSubscriber,
                   configure_logging,
                   namespace_name,
                   string_message_handler,
                   subscription_name,
                   topic_name)

# Connection String Based Publisher If It Set to True Otherwise Default Azure Login
USE_CONNECTION_STR = False

NAMESPACE = namespace_name()
TOPIC = topic_name()
SUBSCRIPTION_NAME = subscription_name()

SUBSCRIBER = ServiceBusSubscriber(namespace=NAMESPACE,
                                  queue_or_topic_name=TOPIC,
                                  strategy=TopicMessageReceiverStrategy,
                                  use_connection_str=USE_CONNECTION_STR)


async def main():
    await SUBSCRIBER.start_listening(message_handler=string_message_handler,
                               subscription_name=SUBSCRIPTION_NAME)
    if isinstance(SUBSCRIBER.factory_object, ServiceBusClientFactory):
        await SUBSCRIBER.factory_object._credential.close()
    


if __name__ == "__main__":
    configure_logging()
    logging.getLogger('azure').setLevel(logging.WARNING)

    asyncio.run(main())
