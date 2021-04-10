from datetime import datetime, timedelta

from django.db.models import Count
import dateutil.parser
from .serializers import PlantSerializer, SoilFertitlityBordersSerializer, SoilMoistureBordersSerializer, \
    SunlightIntensityBordersSerializer, TemperatureBordersSerializer, LocationsSerializer, PlantDataSerializer, ValueChangesSerializer
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders, Locations, PlantData, ValueChanges


def get_plant_details(plantdata, plant_id):
    plant = Plant.objects.filter(id=plant_id).first()
    soil_fertitlity_borders = SoilFertitlityBorders.objects.get(plant_id=plant.id)
    soil_moisture_borders = SoilMoistureBorders.objects.get(plant_id=plant.id)
    sunlight_intensity_borders = SunlightIntensityBorders.objects.get(plant_id=plant.id)
    temperature_borders = TemperatureBorders.objects.get(plant_id=plant.id)

    plant_data_serialized = PlantDataSerializer(plantdata).data
    plant_serialized = PlantSerializer(plant).data
    soil_fertitlity_borders_serializer = SoilFertitlityBordersSerializer(soil_fertitlity_borders)
    soil_moisture_borders = SoilMoistureBordersSerializer(soil_moisture_borders)
    sunlight_intensity_borders = SunlightIntensityBordersSerializer(sunlight_intensity_borders)
    temperature_borders = TemperatureBordersSerializer(temperature_borders)

    plant_dict = plant_data_serialized
    plant_dict.update(plant_serialized)
    location = Locations.objects.get(plant_id=plant.id)
    location = LocationsSerializer(location)
    plant_dict["location"] = (location.data)

    plant_dict["soil_fertitlity_borders"] = (soil_fertitlity_borders_serializer.data)
    plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
    plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
    plant_dict["temperature_borders"] = (temperature_borders.data)
    return plant_dict


def get_plant_history(plant_id):

    plant_list = PlantData.objects.filter(plant_id=plant_id).order_by('timestamp')
    plants_dict = {}
    counter = 0
    for plant in plant_list:
        #TODO: History border by maxmium 1 year e.g.

        plantdata = PlantData.objects.filter(plant_id=plant_id, timestamp=plant.timestamp).first()
        plant_dict = get_plant_details(plantdata, plant.plant_id)
        #print("-----------------------------" + str(counter) + "-------------------")
        plants_dict[counter] = plant_dict
        #TODO bugfix: that is just a quick solution
        counter = counter + 1
    plant_id = plant_list[0].plant_id
    #get all entries from the last 7 days  / 7 weeks
    start_seven_days_ago = datetime.now() - timedelta(days=6)
    start_seven_weeks_ago = datetime.now() - timedelta(days=48)
    results_m = ValueChanges.objects.filter(plant_id=plant_id, value="M", date__gte=start_seven_days_ago)
    results_m = [value_changes.date.date() for value_changes in results_m]
    results_f = ValueChanges.objects.filter(plant_id=plant_id, value="F", date__gte=start_seven_weeks_ago)
    results_f = [value_changes.date.date() for value_changes in results_f]

    plants_dict["pastWaterReviewArray"] = get_hits(results_m, 7, start_seven_days_ago, 1)
    plants_dict["pastFertilizerReviewArray"] = get_hits(results_f, 7, start_seven_weeks_ago, 7)

    return plants_dict


def get_hits(result_list, range_in_days, start_datetime, interval):
    past_reviews = []
    #TODO: bugfix for weeks than range of 7 days counts as hit
    for x in range(range_in_days):
        if interval == 1 and start_datetime.date() in result_list:
            print("hit = 1")
            past_reviews.append(1)
        elif interval == 7 and any(date in result_list for date in [start_datetime.date() + timedelta(days=x) for x in range(interval)]):
            print("hit = 1")
            past_reviews.append(1)
        else:
            print("no hit = 0")
            past_reviews.append(0)
        start_datetime += timedelta(days=interval)
    return past_reviews


def get_all_plant_details():
    # get all unique IDs
    plant_list_id = Plant.objects.values('id').distinct()
    plants_dict = []
    for plant_id_dic in plant_list_id:
        try:
            plant_id = plant_id_dic['id']

            #TODO: use get_plant_details
            plantdata = PlantData.objects.filter(plant_id=plant_id).latest('timestamp')
            plant = Plant.objects.filter(id=plant_id).first()
            soil_fertitlity_borders = SoilFertitlityBorders.objects.get(plant_id=plant.id)
            soil_moisture_borders = SoilMoistureBorders.objects.get(plant_id=plant.id)
            sunlight_intensity_borders = SunlightIntensityBorders.objects.get(plant_id=plant.id)
            temperature_borders = TemperatureBorders.objects.get(plant_id=plant.id)

            plant_data_serialized = PlantDataSerializer(plantdata).data
            plant_serialized = PlantSerializer(plant).data

            soil_fertitlity_borders_serializer = SoilFertitlityBordersSerializer(soil_fertitlity_borders)
            soil_moisture_borders = SoilMoistureBordersSerializer(soil_moisture_borders)
            sunlight_intensity_borders = SunlightIntensityBordersSerializer(sunlight_intensity_borders)
            temperature_borders = TemperatureBordersSerializer(temperature_borders)
            plant_dict = plant_data_serialized
            plant_dict.update(plant_serialized)
            location = Locations.objects.get(plant_id=plant.id)
            location = LocationsSerializer(location)
            plant_dict["location"] = (location.data)

            plant_dict["soil_fertitlity_borders"] = (soil_fertitlity_borders_serializer.data)
            plant_dict["soil_moisture_borders"] = (soil_moisture_borders.data)
            plant_dict["sunlight_intensity_borders"] = (sunlight_intensity_borders.data)
            plant_dict["temperature_borders"] = (temperature_borders.data)
            plants_dict.append(plant_dict)
        except Exception as e:
            print(e)
            continue
    return plants_dict


def checkup_plant_data(new_plant_data, old_plant_data):
    print("--------------")
    print(str(new_plant_data['soil_moisture']) + " == ?" + str(old_plant_data['soil_moisture']))


    if data_checkup(new_plant_data['soil_moisture'], old_plant_data['soil_moisture'], 2):
        new_entry_date = dateutil.parser.parse(new_plant_data['timestamp'])
        if not ValueChanges.objects.filter(date__date=new_entry_date.date(), value="M", plant_id=new_plant_data["plant_id"]).first():
            related_plant = Plant.objects.filter(id=new_plant_data['plant_id']).first()
            ValueChanges.objects.create(value="M", date=new_plant_data['timestamp'], plant=related_plant)

    if data_checkup(new_plant_data['soil_fertility'], old_plant_data['soil_fertility'], 2):
        new_entry_date = dateutil.parser.parse(new_plant_data['timestamp'])
        if not ValueChanges.objects.filter(date__date=new_entry_date.date(), value="F").first():
            related_plant = Plant.objects.filter(id=new_plant_data['plant_id']).first()
            ValueChanges.objects.create(value="F", date=new_plant_data['timestamp'], plant=related_plant)


# Rvalidate trend of the current data
# for later if check up true or false you can see the trend
def data_checkup(new_data, old_data, threshold):
    if int(new_data) > int(old_data) + threshold:
        return True
    return False

