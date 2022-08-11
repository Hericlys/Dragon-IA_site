from django.db import models
from django.contrib.auth.models import User
from  django.utils import timezone
from datetime import date, timedelta


class Chave(models.Model):

    chave = models.CharField(max_length=255)
    usuario = models.ForeignKey(User, blank=True, on_delete=models.DO_NOTHING)
    data_criacao = models.DateTimeField(default=timezone.now)
    data_expiracao = models.DateTimeField(default=timezone.now)
    r_geral = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    r_mensal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    r_semanal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    r_diario = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.chave
