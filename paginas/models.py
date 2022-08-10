from django.db import models
from django.contrib.auth.models import User
from  django.utils import timezone
from datetime import date, timedelta


class Chave(models.Model):

    chave = models.CharField(max_length=255)
    usuario = models.OneToOneField(User, blank=True, on_delete=models.DO_NOTHING)
    _status = bool("True" if usuario != '' else "False")
    status = models.BooleanField(default=_status)
    data_criacao = models.DateTimeField(default=timezone.now)
    _data_expiracao = timezone.now()+timedelta(days=30)
    data_expiracao = models.DateTimeField(default=_data_expiracao)

    def __str__(self):
        return self.chave
