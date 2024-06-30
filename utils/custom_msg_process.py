import logging

from azure.servicebus import ServiceBusReceivedMessage


async def string_message_handler(message: ServiceBusReceivedMessage) -> None:
    logging.info(f"Received message: {str(message)}")
