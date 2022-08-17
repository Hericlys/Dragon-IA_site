from .models import Paridades
from rest_framework import serializers


class ParidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paridades
        fields = [
            'id',
            'paridade',
            'call',
            'put',
            'payout',
        ]
