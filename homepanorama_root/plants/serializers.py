from rest_framework import serializers
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders

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
        fields = ('address', 'battery', 'name', 'plant_id', 'soil_fertility','soil_moisture', 'sunlight', 'temperature', 'timestamp', 'version')
        depth = 3

class PlantDetailSerializer(serializers.HyperlinkedModelSerializer):
    soil_fertitlity_borders = SoilFertitlityBordersSerializer(many=False)
    soil_moisture_borders = SoilMoistureBordersSerializer(many=False)
    sunlight_intensity_borders = SunlightIntensityBordersSerializer(many=False)
    temperature_borders = TemperatureBordersSerializer(many=False)
    plant = PlantSerializer(many=False)
    class Meta:
        model = Plant
        fields = ('plant')
        depth = 3
