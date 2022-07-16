from rest_framework import serializers
from .models import *

class DialCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialCodeModels
        fields = '__all__'