from typing import Dict

from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient


class ServiceBusClientFactory:
    _instances: Dict[str, ServiceBusClient] = {}

    @staticmethod
    async def get_client(namespace: str) -> ServiceBusClient:
        credential = DefaultAzureCredential()

        if namespace not in ServiceBusClientFactory._instances:
            ServiceBusClientFactory._instances[namespace] = ServiceBusClient(fully_qualified_namespace=namespace,
                                                                             credential=credential)
        return ServiceBusClientFactory._instances[namespace]
