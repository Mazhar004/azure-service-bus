import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

from azure.servicebus import ServiceBusReceivedMessage
from azure.servicebus.aio import ServiceBusClient, ServiceBusReceiver


class MessageReceiverStrategy(ABC):
    @abstractmethod
    async def subscribing_messages(self,
                                   client: ServiceBusClient,
                                   name: str,
                                   message_handler: Callable[[ServiceBusReceivedMessage], None],
                                   subscription_name: Optional[str] = None) -> None:
        pass

    async def process_messages(self, receiver: ServiceBusReceiver,
                               message_handler: Callable[[ServiceBusReceivedMessage], None],
                               source: str) -> None:
        EMPTY_MESSAGES_THRESHOLD = 10
        PULLING_FREQUENCY_SECONDS = 5

        empty_messages_count = 0

        while True:
            received_msgs = await receiver.receive_messages(max_wait_time=5,
                                                            max_message_count=20)
            if received_msgs:
                for msg in received_msgs:
                    await message_handler(msg)
                    await receiver.complete_message(msg)

                empty_messages_count = 0
                continue

            empty_messages_count += 1
            logging.info(f'No messages received from {source}, empty count: {empty_messages_count}')

            if empty_messages_count >= EMPTY_MESSAGES_THRESHOLD:
                logging.info(f'Empty messages count threshold reached, exiting...')
                break

            logging.info(f'No messages received from {source}, sleeping... for {PULLING_FREQUENCY_SECONDS} seconds')
            await asyncio.sleep(PULLING_FREQUENCY_SECONDS)


class QueueMessageReceiverStrategy(MessageReceiverStrategy):
    async def subscribing_messages(self,
                                   client: ServiceBusClient,
                                   name: str,
                                   message_handler: Callable[[ServiceBusReceivedMessage], None],
                                   subscription_name: Optional[str] = None) -> None:
        async with client.get_queue_receiver(queue_name=name,
                                             max_wait_time=5) as receiver:
            logging.info("Listening.. to queue")
            await self.process_messages(receiver, message_handler, "queue")


class TopicMessageReceiverStrategy(MessageReceiverStrategy):
    async def subscribing_messages(self,
                                   client: ServiceBusClient,
                                   name: str,
                                   message_handler: Callable[[ServiceBusReceivedMessage], None],
                                   subscription_name: Optional[str] = None) -> None:
        async with client.get_subscription_receiver(topic_name=name,
                                                    subscription_name=subscription_name,
                                                    max_wait_time=5) as receiver:
            logging.info("Listening.. to topic")
            await self.process_messages(receiver, message_handler, "topic")
