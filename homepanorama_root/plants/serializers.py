from rest_framework import serializers
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders, PlantData, Locations


class SoilFertitlityBordersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilFertitlityBorders
        fields = ('currency', 'min', 'max')


class SoilMoistureBordersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SoilMoistureBorders
        fields = ('currency', 'min', 'max')


class SunlightIntensityBordersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SunlightIntensityBorders
        fields = ('currency', 'min', 'max')


class TemperatureBordersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TemperatureBorders
        fields = ('currency', 'min', 'max')


class PlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plant
        fields = (
            'id', 'name', 'address', 'version')


class PlantDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlantData
        fields = (
            'battery', 'soil_fertility', 'soil_moisture', 'sunlight', 'temperature',
            'timestamp')
        #depth = 3


class LocationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locations
        fields = ('location', 'location_details')