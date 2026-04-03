from rest_framework import serializers
from .models import Mission


class MissionSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.id')

    class Meta:
        model = Mission
        fields = '__all__'

