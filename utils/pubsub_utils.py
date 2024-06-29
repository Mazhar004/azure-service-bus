import logging
from typing import Callable, List, Union

from azure.servicebus import ServiceBusReceivedMessage
from client import ServiceBusClientFactory, ServiceBusClientFactoryString
from message import MessageReceiverStrategy, MessageSenderStrategy

from utils import connection_str


class ServiceBusPublisher:
    def __init__(self, namespace: str, strategy: MessageSenderStrategy, use_connection_str: bool = True) -> None:
        self.namespace = namespace
        self.use_connection_str = use_connection_str

        if self.use_connection_str:
            logging.info("Using Connection String")
            self.factory_object = ServiceBusClientFactoryString(connection_str=connection_str())
        else:
            logging.info("Using Default Azure Login")
            self.factory_object = ServiceBusClientFactory()

        self.client = None
        self.strategy: MessageSenderStrategy = strategy()

    async def send_message(self, queue_or_topic_name: str, message_content: Union[str, List[str]]) -> None:
        self.client = await self.factory_object.get_client(namespace=self.namespace)

        async with self.client:
            logging.info(f"Sending message to {queue_or_topic_name}")
            await self.strategy.send_message(client=self.client,
                                             name=queue_or_topic_name,
                                             message_content=message_content)


class ServiceBusSubscriber:
    def __init__(self, namespace: str, queue_or_topic_name: str, strategy: MessageReceiverStrategy, use_connection_str: bool = True) -> None:
        self.namespace = namespace
        self.queue_or_topic_name = queue_or_topic_name
        self.use_connection_str = use_connection_str

        if self.use_connection_str:
            logging.info("Using Connection String")
            self.factory_object = ServiceBusClientFactoryString(connection_str=connection_str())
        else:
            logging.info("Using Default Azure Login")
            self.factory_object = ServiceBusClientFactory()

        self.client = None
        self.strategy: MessageReceiverStrategy = strategy()

    async def start_listening(self,
                              message_handler: Callable[[ServiceBusReceivedMessage], None],
                              subscription_name: str = None) -> None:
        self.client = await self.factory_object.get_client(namespace=self.namespace)

        async with self.client:
            await self.strategy.subscribing_messages(client=self.client,
                                                     name=self.queue_or_topic_name,
                                                     message_handler=message_handler,
                                                     subscription_name=subscription_name)
