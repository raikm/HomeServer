from django.db.models import Count

from plants.serializers import PlantSerializer, SoilFertitlityBordersSerializer, SoilMoistureBordersSerializer, \
    SunlightIntensityBordersSerializer, TemperatureBordersSerializer, LocationsSerializer
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders, Locations


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
    plant_dict["soil_fertitlity_borders"] = (soil_fertitlity_borders_serializer.data)
    plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
    plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
    plant_dict["temperature_borders"] = (temperature_borders.data)
    return plant_dict

def get_plant_details(plant_id, timestamp):
    #print(str(plant_id) + "     " + str(timestamp))
    _plant = Plant.objects.filter(plant_id=plant_id, timestamp=timestamp)
    #TODO: what if more found?
    plant = _plant[0]
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
    plant_dict["soil_fertitlity_borders"] = (soil_fertitlity_borders_serializer.data)
    plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
    plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
    plant_dict["temperature_borders"] = (temperature_borders.data)
    return plant_dict

def get_plant_history(plant_id):
    #("start")
    plant_list = Plant.objects.filter(plant_id=plant_id).order_by('timestamp')
    #print(len(plant_list))
    plants_dict = {}
    counter = 0
    for plant in plant_list:
        #TODO: History border by maxmium 1 year e.g.
        #print("get plant from : " + str(plant.timestamp))
        plant_dict = get_plant_details(plant.plant_id, plant.timestamp)
        #print("-----------------------------" + str(counter) + "-------------------")
        plants_dict[counter] = plant_dict
        #TODO bugfix: that is just a quick solution
        counter = counter + 1
    #print("length = " + str(len(plants_dict)))

    return plants_dict


def get_all_plant_details():
    # get all unique IDs
    plant_list_id = Plant.objects.values('plant_id').distinct()
    plants_dict = {}
    for plant_id_dic in plant_list_id:
        plant_id = plant_id_dic['plant_id']
        #print("prepare Plant with the ID: " + str(plant_id))
        #TODO: use get_plant_details
        plant = Plant.objects.filter(plant_id=plant_id).latest('timestamp')

        soil_fertitlity_borders = SoilFertitlityBorders.objects.get(plant_id=plant_id)
        soil_moisture_borders = SoilMoistureBorders.objects.get(plant_id=plant_id)
        sunlight_intensity_borders = SunlightIntensityBorders.objects.get(plant_id=plant_id)
        temperature_borders = TemperatureBorders.objects.get(plant_id=plant_id)
        location = Locations.objects.get(plant_id=plant_id)

        plant_serializer = PlantSerializer(plant)
        soil_fertitlity_borders_serializer = SoilFertitlityBordersSerializer(soil_fertitlity_borders)
        soil_moisture_borders = SoilMoistureBordersSerializer(soil_moisture_borders)
        sunlight_intensity_borders = SunlightIntensityBordersSerializer(sunlight_intensity_borders)
        temperature_borders = TemperatureBordersSerializer(temperature_borders)
        location = LocationsSerializer(location)
        plant_dict = plant_serializer.data
        plant_dict["soil_fertitlity_borders"] = (soil_fertitlity_borders_serializer.data)
        plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
        plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
        plant_dict["temperature_borders"] = (temperature_borders.data)
        plant_dict["location"] = (location.data)
        plants_dict[plant_serializer.data['name']] = plant_dict

    return plants_dict
