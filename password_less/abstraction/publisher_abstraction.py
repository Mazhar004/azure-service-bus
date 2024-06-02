import logging
from abc import ABC, abstractmethod
from typing import List, Union

from azure.servicebus import ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient, ServiceBusSender
from azure.servicebus.exceptions import MessageSizeExceededError


class MessageSenderStrategy(ABC):
    @abstractmethod
    async def send_message(self, client: ServiceBusClient, name: str, message_content: Union[str, List[str]]) -> None:
        """Send a message or a list of messages."""
        pass

    async def send_single_message(self, sender: ServiceBusSender, message_content: str) -> None:
        """Send a single message."""
        message = ServiceBusMessage(message_content)
        await sender.send_messages(message)
        logging.info(f"Sent a single {message_content=}")

    async def send_batch_message(self, sender: ServiceBusSender, message_list: List[str]) -> None:
        """Send a batch of messages."""
        async with sender:
            batch_message = await sender.create_message_batch()
            for msg in message_list:
                try:
                    batch_message.add_message(ServiceBusMessage(msg))
                except MessageSizeExceededError:
                    # ServiceBusMessageBatch object reaches max_size.
                    logging.info(f"Batch message is full. Sending..")
                    await sender.send_messages(batch_message)
                    batch_message = await sender.create_message_batch()
                    batch_message.add_message(ServiceBusMessage(msg))
            await sender.send_messages(batch_message)
        logging.info(f"Sent a list of {len(message_list)} {message_list=}")


class QueueMessageSenderStrategy(MessageSenderStrategy):
    async def send_message(self, client: ServiceBusClient, name: str, message_content: Union[str, List[str]]) -> None:
        """Send a message or a list of messages to a queue."""
        async with client.get_queue_sender(queue_name=name) as sender:
            logging.info("Sending.. message to queue")

            if isinstance(message_content, List):
                await self.send_batch_message(sender, message_content)
            else:
                await self.send_single_message(sender, message_content)


class TopicMessageSenderStrategy(MessageSenderStrategy):
    async def send_message(self, client: ServiceBusClient, name: str, message_content: Union[str, List[str]]) -> None:
        """Send a message or a list of messages to a topic."""
        async with client.get_topic_sender(topic_name=name) as sender:
            logging.info("Sending.. message to topic")

            if isinstance(message_content, List):
                await self.send_batch_message(sender, message_content)
            else:
                await self.send_single_message(sender, message_content)