import pytz

from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .plant_utils import get_plant_details, get_all_plant_details, get_plant_history, checkup_plant_data, data_cleanup
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders, \
    Locations
import pexpect
from datetime import date
from datetime import datetime, timedelta
today = date.today()
midnight = datetime.combine(today, datetime.min.time()) + timedelta(minutes=-5)

@csrf_exempt
@api_view(('PUT', 'GET'))
def plant_detail(request, plant_id):
    if request.method == 'GET':
        # TODO: modify methode
        plant_dict = get_plant_details(plant_id)

        return JsonResponse(plant_dict, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        plant_json = request.data
        last_sunlight_data = 0
        if PlantData.objects.filter(plant_id=plant_json["plant_id"]).first():
            plantdata = PlantData.objects.filter(plant_id=plant_json["plant_id"]).latest('timestamp')
            if check_for_reset(plant_json["plant_id"]) is False:
                last_sunlight_data = plantdata.sunlight
            last_documented_plant_data = get_plant_details(plantdata, plant_json["plant_id"])
            checkup_plant_data(plant_json, last_documented_plant_data)
        plant = Plant.objects.filter(id=plant_json["plant_id"]).first()
        data_cleanup(plant.id)
        try:

            PlantData.objects.create(battery=plant_json["battery"], soil_fertility=plant_json["soil_fertility"],
                                     soil_moisture=plant_json["soil_moisture"], sunlight=last_sunlight_data + int(plant_json["sunlight"]),
                                     temperature=plant_json["temperature"], timestamp=plant_json["timestamp"],
                                     plant=plant)
        except:
            return Response("error while saving data update", status=status.HTTP_400_BAD_REQUEST)

        return Response("new data update saved", status=status.HTTP_201_CREATED)

# @csrf_exempt
# @api_view(('GET',))
# def get_all_plants_with_details(request):
#     plant_list_id = Plant.objects.values('id').distinct()
#     result = []
#     for plant_id_dic in plant_list_id:
#         plant_id = plant_id_dic['id']
#         result.append(get_all_plant_details())
#
#     return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET',))
def get_all_plant_data(request):
    # get all plants (latest included the details)
    # TODO: modify methode
    result = get_all_plant_details()
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET',))
def get_all_plants(request):
    plant_qs = Plant.objects.all()
    plant_list = []
    for plant in plant_qs:
        plant_serialized = PlantSerializer(plant).data
        plant_location_qs = Locations.objects.get(plant_id=plant.id)
        plant_location_serialized = LocationsSerializer(plant_location_qs).data
        plant_serialized["location"] = plant_location_serialized
        plant_list.append(plant_serialized)
    return Response(plant_list, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(('GET',))
def get_latest_plant_updates(request):
    plant_list = Plant.objects.all()
    plant_list_result = []
    for plant in plant_list:
        try:
            plantdata = PlantData.objects.filter(plant_id=plant.id).latest('timestamp')
            plant_list_result.append(get_plant_details(plantdata, plant.id))
        except PlantData.DoesNotExist:
            print("skip plant data since no data yet fetched")
    return Response(plant_list_result, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(('GET',))
def plant_detail_history(request, plant_id, hours):
    result = get_plant_history(plant_id, hours)
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET',))
def reload_plant_data(request):
    print("start")
    ssh_newkey = 'Are you sure you want to continue connecting'
    child = pexpect.spawn('ssh hoobs@192.168.1.79 sudo python3 /AutomationTools/Tools/miflora_reader.py')
    i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    if i == 0:  # Timeout
        print('ERROR!')
        print('SSH could not login. Here is what SSH said:')
        print(child.before, child.after)
        return None
    if i == 1:  # SSH does not have the public key. Just accept it.
        child.sendline('yes')
        child.expect('password: ')
        i = child.expect([pexpect.TIMEOUT, 'password: '])
        if i == 0:  # Timeout
            print('9ERROR!')
            print('SSH could not login. Here is what SSH said:')
            print(child.before, child.after)
            return None
    # TODO: use config
    child.sendline('hoobsadmin')
    child.expect(pexpect.EOF, timeout=120)
    output = child.before
    print(output)

    result = get_all_plant_details()
    print(result)
    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
@api_view(('PUT',))
def create_update_plant(request, plant_id):
    if request.method == 'PUT':
        plant_json = request.data
        print(plant_json)

        if (Plant.objects.filter(id=plant_id).first() is not None):
            print("update exisiting plant")
            Plant.objects.filter(id=plant_id).update(name=plant_json["name"], address=plant_json["address"])
        else:
            print("create exisiting plant")
            Plant.objects.create(id=plant_id, name=plant_json["name"], address=plant_json["address"])

        SoilFertitlityBorders.objects.filter(plant_id=plant_id).update_or_create(
            min=plant_json["soil_fertitlity_borders"]["min"], max=plant_json["soil_fertitlity_borders"]["max"],
            currency=plant_json["soil_fertitlity_borders"]["currency"])
        SoilMoistureBorders.objects.filter(plant_id=plant_id).update_or_create(
            min=plant_json["soil_moisture_borders"]["min"],
            max=plant_json["soil_moisture_borders"]["max"],
            currency=plant_json["soil_moisture_borders"][
                "currency"])
        SunlightIntensityBorders.objects.filter(plant_id=plant_id).update_or_create(
            min=plant_json["sunlight_intensity_borders"]["min"],
            max=plant_json["sunlight_intensity_borders"]["max"],
            currency=plant_json["sunlight_intensity_borders"][
                "currency"])
        TemperatureBorders.objects.filter(plant_id=plant_id).update_or_create(
            min=plant_json["temperature_borders"]["min"],
            max=plant_json["temperature_borders"]["max"],
            currency=plant_json["temperature_borders"][
                "currency"])
        Locations.objects.filter(plant_id=plant_id).update_or_create(location=plant_json["location"]["location"],
                                                           location_details=plant_json["temperature_borders"][
                                                               "max"])


            # return Response("error while updating plant", status=status.HTTP_400_BAD_REQUEST)
        return Response("plant got updated", status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET',))
def get_new_id(request):
    plants_desc_ids = Plant.objects.order_by('-id')
    last_plant = plants_desc_ids[0]
    new_id = last_plant.id + 1
    return JsonResponse(new_id, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
@api_view(('GET',))
def get_not_set_mac_addresses(request):
    print("start")
    #restart_bluetooth_service()
    output = get_address()
    print(output)
    return JsonResponse("OK", status=status.HTTP_200_OK, safe=False)

#
# def get_address():
#     ssh_newkey = 'Are you sure you want to continue connecting'
#     child = pexpect.spawn('ssh hoobs@192.168.1.79 sudo hciconfig hci0 reset; sudo timeout -s SIGINT 30s hcitool -i hci0 lescan')
#     i = child.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
#     if i == 0:  # Timeout
#         print('ERROR!')
#         print('SSH could not login. Here is what SSH said:')
#         print(child.before, child.after)
#         return None
#     if i == 1:  # SSH does not have the public key. Just accept it.
#         child.sendline('yes')
#         child.expect('password: ')
#         i = child.expect([pexpect.TIMEOUT, 'password: '])
#         if i == 0:  # Timeout
#             print('ERROR!')
#             print('SSH could not login. Here is what SSH said:')
#             print(child.before, child.after)
#             return None
#     # TODO: use config
#     child.sendline('hoobsadmin')
#     child.expect(pexpect.EOF, timeout=120)
#     output = child.before
#     return output

def check_for_reset(plant_id):
    print("check for reset at " + str(datetime.now(tz=pytz.timezone('Europe/Berlin'))))
    print("midnight: " + str(midnight))
    result = PlantData.objects.filter(plant_id=plant_id).filter(timestamp__gt=midnight).count()
    print("result: " + str(result))
    if result == 0:
        return True
    return False
