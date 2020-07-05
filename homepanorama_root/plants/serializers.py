from rest_framework import serializers
from .models import Plant

class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScriptStatus
        fields = ('plant_id', 'plantname', 'battery', 'version', 'sunlight', 'temperature', 'moisture', 'fertility', 'timestamp')
