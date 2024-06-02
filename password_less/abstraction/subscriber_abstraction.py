import logging
from abc import ABC, abstractmethod
from typing import Callable, Optional

from azure.servicebus import ServiceBusReceivedMessage
from azure.servicebus.aio import ServiceBusClient, ServiceBusReceiver
import asyncio

class MessageReceiverStrategy(ABC):
    @abstractmethod
    async def subscribing_messages(self,
                                   client: ServiceBusClient,
                                   name: str,
                                   message_handler: Callable[[ServiceBusReceivedMessage], None],
                                   subscription_name: Optional[str] = None) -> None:
        pass
