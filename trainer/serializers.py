from rest_framework import serializers

from .models import *


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['profile', 'id', 'message', 'phone', 'email', 'read', 'dttime']
