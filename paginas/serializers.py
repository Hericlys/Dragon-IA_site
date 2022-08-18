from .models import Paridades
from rest_framework import serializers


class ParidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paridades
        fields = [
            'paridade',
            'call',
            'put',
            'payout',
            'analise',
        ]
