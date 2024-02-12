from django.db import models


class Client(models.Model):
    phone_number = models.IntegerField(unique=True)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.phone_number)
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
