from django.shortcuts import render
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders
from .serializers import PlantSerializer, SoilFertitlityBordersSerializer, SoilMoistureBordersSerializer, SunlightIntensityBordersSerializer, TemperatureBordersSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .plant_utils import get_plant_details, get_all_plant_details

@csrf_exempt
@api_view(('PUT', 'GET'))
def plant_detail(request, plant_id):
    if request.method == 'GET':
        plant_dict = get_plant_details(plant_id)
        return JsonResponse(plant_dict, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        print(request.data)
        serializer = PlantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(('GET', ))
def all_plants(request):
    # get all plants (latest included the details)
    result = get_all_plant_details()
    print (result)
    return JsonResponse(result, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(('GET', ))
def plant_detail_history(request, plant_id):
    pass
