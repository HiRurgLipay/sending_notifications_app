from datetime import datetime
import logging
from typing import Dict

from django.utils.timezone import make_aware
from django.utils import timezone
from django.db import transaction

from core.models import Mailing
from core.tasks import send_messages_task


logger = logging.getLogger(__name__)


@transaction.atomic
def create_mailing_service(mailing_data: Dict[str, str]) -> Mailing:
    try:
        start_datetime = mailing_data.get('start_datetime')
        end_datetime = mailing_data.get('end_datetime')

        # Проверяем, есть ли даты начала и окончания рассылки в данных
        if start_datetime and end_datetime:
            # Преобразуем строки в объекты datetime.datetime
            start_datetime = make_aware(datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S'))
            end_datetime = make_aware(datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M:%S'))
            
            # Создаем рассылку
            mailing = Mailing.objects.create(**mailing_data)
            
            # Проверяем, нужно ли немедленно запускать рассылку
            if start_datetime <= timezone.now() < end_datetime:
                logger.info(f"Сreated new mailing: {mailing}")
                send_messages_task.delay(mailing.id)
                
            # Если время начала рассылки в будущем, запускаем задачу по наступлению этого времени
            elif start_datetime > timezone.now():
                logger.info(f"Сreated new mailing: {mailing} | Mailing is going to start at {start_datetime}")
                send_messages_task.apply_async((mailing.id,), eta=start_datetime)
                
            return mailing
        else:
            raise ValueError("start_datetime and end_datetime are required fields")
    except Exception as e:
        logger.error(f"Failed to create mailing: {e}")
        raise


def update_mailing_service(mailing_id: int, updated_data: Dict[str, str]) -> Mailing:
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
        for key, value in updated_data.items():
            setattr(mailing, key, value)
        mailing.save()
        logger.info(f"Updated mailing with ID {mailing_id}: {mailing}")
        return mailing
    except Exception as e:
        logger.error(f"Failed to update mailing with ID {mailing_id}: {e}")
        raise


def delete_mailing_service(mailing_id: int) -> None:
    try:
        mailing = Mailing.objects.get(pk=mailing_id)
        mailing.delete()
        logger.info(f"Deleted mailing with ID {mailing_id}")
    except Exception as e:
        logger.error(f"Failed to delete mailing with ID {mailing_id}: {e}")
        raise
