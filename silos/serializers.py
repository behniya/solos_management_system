from rest_framework import serializers
from .models import Silo, SiloLog

class SiloLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiloLog
        fields = ['id', 'change_type', 'amount', 'timestamp', 'silo']
        read_only_fields = ['id', 'timestamp', 'silo']

    def create(self, validated_data):
        silo = self.context['silo']
        validated_data['silo'] = silo
        return super().create(validated_data)

class SiloSerializer(serializers.ModelSerializer):
    logs = SiloLogSerializer(many=True, read_only=True)

    class Meta:
        model = Silo
        fields = ['id', 'name', 'capacity', 'current_stock', 'logs']
