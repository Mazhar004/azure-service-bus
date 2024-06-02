from typing import Callable, List, Union

from client import ServiceBusClientFactory
from message import MessageReceiverStrategy, MessageSenderStrategy


from azure.identity.aio import DefaultAzureCredential
from azure.servicebus import ServiceBusReceivedMessage


class ServiceBusPublisher:
    def __init__(self, namespace: str, queue_or_topic_name: str, strategy: MessageSenderStrategy) -> None:
        self.namespace = namespace
        self.queue_or_topic_name = queue_or_topic_name

        self.client = None
        self.strategy: MessageSenderStrategy = strategy()

    async def send_message(self, message_content: Union[str, List[str]]) -> None:
        if self.client is None:
            self.client = await ServiceBusClientFactory.get_client(namespace=self.namespace)

        async with self.client:
            await self.strategy.send_message(client=self.client,
                                             name=self.queue_or_topic_name,
                                             message_content=message_content)


class ServiceBusSubscriber:
    def __init__(self, namespace: str, queue_or_topic_name: str, strategy: MessageReceiverStrategy) -> None:
        self.namespace = namespace
        self.queue_or_topic_name = queue_or_topic_name

        self.client = None
        self.strategy: MessageReceiverStrategy = strategy()

    async def start_listening(self,
                              message_handler: Callable[[ServiceBusReceivedMessage], None],
                              subscription_name: str = None) -> None:

        if self.client is None:
            self.client = await ServiceBusClientFactory.get_client(namespace=self.namespace)

        async with self.client:
            await self.strategy.subscribing_messages(client=self.client,
                                                     name=self.queue_or_topic_name,
                                                     message_handler=message_handler,
                                                     subscription_name=subscription_name)
