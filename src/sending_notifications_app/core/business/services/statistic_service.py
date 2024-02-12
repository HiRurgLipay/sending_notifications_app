from django.shortcuts import get_object_or_404
import logging
from typing import List, Dict

from core.models import Mailing, Message


logger = logging.getLogger(__name__)


def get_mailing_statistics_service(mailing_id: int) -> Dict[str, int]:
    mailing = get_object_or_404(Mailing, id=mailing_id)
    messages = Message.objects.filter(mailing=mailing)

    statistics = {
        'mailing_id': mailing_id,
        'total_messages': messages.count(),
        'pending_messages': messages.filter(status='pending').count(),
        'sent_messages': messages.filter(status='sent').count(),
        'failed_messages': messages.filter(status='failed').count()
    }

    return statistics


def get_detailed_message_statistics_service(mailing_id: int) -> List[Dict[str, any]]:
    mailing = get_object_or_404(Mailing, id=mailing_id)
    messages = Message.objects.filter(mailing=mailing)

    detailed_statistics = []
    for message in messages:
        message_data = {
            'message_id': message.id,
            'client_phone': message.client.phone_number,
            'status': message.status
        }
        detailed_statistics.append(message_data)

    return detailed_statistics
