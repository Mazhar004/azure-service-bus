import argparse
import asyncio
import logging

# Azure
from azure.identity.aio import DefaultAzureCredential

# Customs
from abstraction import TopicMessageSenderStrategy
from auth import namespace_name, topic_name
from pubsub_utils import ServiceBusPublisher


publisher = ServiceBusPublisher(namespace=namespace_name(),
                                queue_or_topic_name=topic_name(),
                                strategy=TopicMessageSenderStrategy)


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
        publisher = Publisher(fully_qualified_namespace=FULLY_QUALIFIED_NAMESPACE,
                              topic_name=TOPIC_NAME)

        if args.pubsub:
            asyncio.run(publisher.publish(args.msg))
        else:
            logger.info(f"Logging message: {args.msg}")
