from django.shortcuts import render
from .models import Plant, SoilFertitlityBorders, SoilMoistureBorders, SunlightIntensityBorders, TemperatureBorders
from .serializers import PlantSerializer, SoilFertitlityBordersSerializer, SoilMoistureBordersSerializer, SunlightIntensityBordersSerializer, TemperatureBordersSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse

@csrf_exempt
@api_view(('PUT', 'GET'))
def plant_detail(request, plant_id):
    if request.method == 'GET':
        #TODO: get plantdata what is UP TO DATE
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
        return JsonResponse(plant_dict, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        print(request.data)
        serializer = PlantSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(('GET'))
def all_plants(request):
    pass


@csrf_exempt
@api_view(('GET'))
def plant_detail_history(request, plant_id):
    pass
