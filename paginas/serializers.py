from .models import Paridades, Chave
from rest_framework import serializers


class ParidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paridades
        fields = [
            'paridade',
            'call',
            'put',
        ]


class ChaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chave
        fields = [
            'chave',
        ]
