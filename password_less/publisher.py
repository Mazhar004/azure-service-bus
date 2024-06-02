import argparse
import asyncio
import logging

# Azure
from azure.identity.aio import DefaultAzureCredential

# Customs
from abstraction import TopicMessageSenderStrategy
from auth import namespace_name, topic_name
from pubsub_utils import ServiceBusPublisher


async def publish_message(message: str) -> None:
    await publisher.send_message([message, message])
    logging.info("Message was published successfully.")


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
        publisher = ServiceBusPublisher(namespace=namespace_name(),
                                        queue_or_topic_name=topic_name(),
                                        strategy=TopicMessageSenderStrategy)

        if args.pubsub:
            asyncio.run(publish_message(args.msg))
        else:
            logging.info(f"Logging message: {args.msg}")


if __name__ == "__main__":
    main()
