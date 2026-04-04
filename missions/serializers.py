from rest_framework import serializers
from .models import Mission, MissionApplication


class MissionSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.id')

    class Meta:
        model = Mission
        fields = '__all__'

class MissionApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionApplication
        fields = "__all__"
        read_only_fields = ("freelancer", "status", "created_at", "mission")


