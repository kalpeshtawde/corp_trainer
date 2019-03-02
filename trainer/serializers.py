from rest_framework import serializers

from .models import *


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['user', 'id', 'message', 'phone', 'email', 'read', 'dttime']


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['locations', 'hours_per_week']
