from django.db import models
from django.utils import timezone


class Mailing(models.Model):
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField()
    message_text = models.TextField()
    operator_code_filter = models.CharField(max_length=10)
    tag_filter = models.CharField(max_length=100)

    def __str__(self):
        return self.message_text
    
    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
