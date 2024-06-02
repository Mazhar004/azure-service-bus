import asyncio
import logging

from abstraction import TopicMessageReceiverStrategy
from auth import namespace_name, subscription_name, topic_name
from pubsub_utils import ServiceBusSubscriber

from utils import string_message_handler

subscriber = ServiceBusSubscriber(namespace=namespace_name(),
                                  queue_or_topic_name=topic_name(),
                                  strategy=TopicMessageReceiverStrategy)


def main():
    asyncio.run(subscriber.start_listening(message_handler=string_message_handler,
                                           subscription_name=subscription_name()
                                           )
                )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.getLogger('azure').setLevel(logging.WARNING)
    main()
