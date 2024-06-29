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
        logging.info(f"Sent a single message.")

    async def send_batch_message(self, sender: ServiceBusSender, message_list: List[str]) -> None:
        """Send a batch of messages."""
        MAX_BATCH_SIZE = 256 * 1024
        async with sender:
            batch_message = await sender.create_message_batch(max_size_in_bytes=MAX_BATCH_SIZE)

            for msg in message_list:
                message = ServiceBusMessage(msg)
                try:
                    batch_message.add_message(message)
                except MessageSizeExceededError:
                    logging.info(f"Batch message is full. Sending..")
                    await sender.send_messages(batch_message)

                    batch_message = await sender.create_message_batch(max_size_in_bytes=MAX_BATCH_SIZE)
                    batch_message.add_message(message)

            if len(batch_message) > 0:
                await sender.send_messages(batch_message)

        logging.info(f"Sent batche message, total {len(message_list)} messgaes.")


class TopicMessageSenderStrategy(MessageSenderStrategy):
    async def send_message(self, client: ServiceBusClient, name: str, message_content: Union[str, List[str]]) -> None:
        """Send a message or a list of messages to a topic."""
        async with client.get_topic_sender(topic_name=name) as sender:
            logging.info("Sending.. message to topic")

            if isinstance(message_content, List):
                await self.send_batch_message(sender, message_content)
            else:
                await self.send_single_message(sender, message_content)
