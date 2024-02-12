import logging
from typing import Dict

from core.models import Client


logger = logging.getLogger(__name__)

def create_client_service(client_data: Dict[str, str]) -> Client:
    try:
        client = Client.objects.create(**client_data)
        logger.info(f"Created new client: {client}")
        return client
    except Exception as e:
        logger.error(f"Failed to create client: {e}")
        raise

def update_client_service(client_id: int, client_data: Dict[str, str]) -> Client:
    try:
        client = Client.objects.get(pk=client_id)
        for key, value in client_data.items():
            setattr(client, key, value)
        client.save()
        logger.info(f"Updated client with ID {client_id}: {client}")
        return client
    except Exception as e:
        logger.error(f"Failed to update client with ID {client_id}: {e}")
        raise

def delete_client_service(client_id: int) -> None:
    try:
        client = Client.objects.get(pk=client_id)
        client.delete()
        logger.info(f"Deleted client with ID {client_id}")
    except Exception as e:
        logger.error(f"Failed to delete client with ID {client_id}: {e}")
        raise
