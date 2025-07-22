from rest_framework import serializers
from . import models

class TrafficAccidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrafficAccident
        fields = '__all__'


class RainfallRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RainfallRecord
        fields = '__all__'
