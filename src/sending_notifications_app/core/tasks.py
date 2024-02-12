import requests
import os
import logging
from django.db import transaction

from core.models import Mailing, Client, Message
from sending_notifications_app import celery_app


logger = logging.getLogger(__name__)

jwt_token = os.environ["JWT_TOKEN"]

@celery_app.task
def send_messages_task(mailing_id: int) -> None:
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
        clients = Client.objects.filter(operator_code=mailing.operator_code_filter, tag=mailing.tag_filter)
    except Mailing.DoesNotExist:
        logger.error(f"Mailing with id {mailing_id} does not exist")
        return
    except Client.DoesNotExist:
        logger.error("No clients match the filter criteria")
        return
    
    successful_count = 0
    failed_count = 0
    
    for client in clients:
        message_text = mailing.message_text
        phone_number = client.phone_number
        client_id = client.id
        
        url = f'https://probe.fbrq.cloud/v1/send/{mailing_id}'
        payload = {
            'id': mailing_id,
            'phone': phone_number,
            'text': message_text
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': jwt_token
        }
        
        try:
            with transaction.atomic():
                message = Message.objects.create(
                    status='pending',
                    mailing_id=mailing_id,
                    client_id=client_id
                )
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    message.status = 'sent'
                    message.save()
                    successful_count += 1
                    logger.info(f"Message sent successfully to {phone_number}")
                else:
                    message.status = 'failed'
                    message.save()
                    failed_count += 1
                    logger.error(f"Failed to send message to {phone_number}. Status code: {response.status_code}")
        except Exception as e:
            logger.exception(f"An error occurred while sending message to {phone_number}: {e}")
            failed_count += 1

    logger.info(f"Mailing {mailing_id} processed. Successful messages: {successful_count}, Failed messages: {failed_count}")
