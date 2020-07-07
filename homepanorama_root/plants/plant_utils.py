from plants.serializers import PlantSerializer, SoilFertitlityBordersSerializer, SoilMoistureBordersSerializer, \
    SunlightIntensityBordersSerializer, TemperatureBordersSerializer
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders


def get_plant_details(plant_id):
    plant = Plant.objects.filter(plant_id=plant_id).latest('timestamp')

    soil_fertitlity_borders = SoilFertitlityBorders.objects.get(plant_id=plant.plant_id)
    soil_moisture_borders = SoilMoistureBorders.objects.get(plant_id=plant.plant_id)
    sunlight_intensity_borders = SunlightIntensityBorders.objects.get(plant_id=plant.plant_id)
    temperature_borders = TemperatureBorders.objects.get(plant_id=plant.plant_id)

    plant_serializer = PlantSerializer(plant)
    soil_fertitlity_borders_serializer = SoilFertitlityBordersSerializer(soil_fertitlity_borders)
    soil_moisture_borders = SoilMoistureBordersSerializer(soil_moisture_borders)
    sunlight_intensity_borders = SunlightIntensityBordersSerializer(sunlight_intensity_borders)
    temperature_borders = TemperatureBordersSerializer(temperature_borders)
    plant_dict = plant_serializer.data
    plant_dict["soil_fertitlity_borders_serializer"] = (soil_fertitlity_borders_serializer.data)
    plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
    plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
    plant_dict["temperature_borders"] = (temperature_borders.data)
    return plant_dict
