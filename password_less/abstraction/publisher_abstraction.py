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
        logging.info("Sent a single message")

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
        logging.info(f"Sent a list of {len(message_list)} messages")


