from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .plant_utils import get_plant_details, get_all_plant_details, get_plant_history, checkup_plant_data
from .models import Plant
import pexpect

@csrf_exempt
@api_view(('PUT', 'GET'))
def plant_detail(request, plant_id):

    if request.method == 'GET':
        #TODO: modify methode
        plant_dict = get_plant_details(plant_id)
        return JsonResponse(plant_dict, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        plant_json = request.data
        print(plant_json)
        plantdata = PlantData.objects.filter(plant_id=plant_json["plant_id"]).latest('timestamp')
        last_documentad_plant_data = get_plant_details(plantdata, plant_json["plant_id"])
        checkup_plant_data(plant_json, last_documentad_plant_data)
        plant = Plant.objects.filter(id=plant_json["plant_id"]).first()
        try:
            PlantData.objects.create(battery = plant_json["battery"],soil_fertility = plant_json["soil_fertility"],soil_moisture = plant_json["soil_moisture"],sunlight = plant_json["sunlight"],temperature = plant_json["temperature"], timestamp = plant_json["timestamp"], plant = plant)
        except:
            return Response("error while saving data update", status=status.HTTP_400_BAD_REQUEST)


        return Response("new data update saved", status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(('GET', ))
def get_all_plant_data(request):
    # get all plants (latest included the details)
    # TODO: modify methode
    result = get_all_plant_details()
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET', ))
def get_all_plants(request):
    plant_list = Plant.objects.all()
    plant_list_result = []
    for plant in plant_list:
        plantdata = PlantData.objects.filter(plant_id=plant.id).latest('timestamp')
        plant_list_result.append(get_plant_details(plantdata, plant.id))
    return Response(plant_list_result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET', ))
def plant_detail_history(request, plant_id):
    result = get_plant_history(plant_id)
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET', ))
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
    #TODO: use config
    child.sendline('hoobsadmin')
    child.expect(pexpect.EOF, timeout=120)
    output = child.before
    print(output)

    result = get_all_plant_details()
    print(result)
    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)