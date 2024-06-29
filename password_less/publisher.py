import argparse
import asyncio
import logging

from client import ServiceBusClientFactory
from message import TopicMessageSenderStrategy

from utils import (ServiceBusPublisher,
                   configure_logging,
                   connection_str,
                   namespace_name,
                   topic_name)

# Connection String Based Publisher
PUBLISHER = ServiceBusPublisher(namespace=namespace_name(),
                                strategy=TopicMessageSenderStrategy,
                                connection_str=connection_str())

# Password Less Publisher with Default Azure Login
# PUBLISHER = ServiceBusPublisher(namespace=namespace_name(),
#                                 strategy=TopicMessageSenderStrategy)
TOPIC = topic_name()


async def publish_message(message: str) -> None:
    await PUBLISHER.send_message(queue_or_topic_name=TOPIC,
                                 message_content=message)
    logging.info("Message was published successfully.")

    if isinstance(PUBLISHER.factory_object, ServiceBusClientFactory):
        await PUBLISHER.factory_object._credential.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--msg",
                        type=str,
                        required=True,
                        help="The message to publish.")
    parser.add_argument("--pubsub",
                        action="store_true",
                        help="If set, publish the message. Otherwise, only log.")
    args = parser.parse_args()

    if args.msg:
        if args.pubsub:
            asyncio.run(publish_message(args.msg))
        else:
            logging.info(f"Logging message: {args.msg}")


if __name__ == "__main__":
    configure_logging()
    logging.getLogger('azure').setLevel(logging.WARNING)

    main()
