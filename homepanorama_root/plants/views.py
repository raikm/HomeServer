from django.shortcuts import render
from .models import Plant
from .serializers import PlantSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@csrf_exempt
@api_view(('PUT', 'GET'))
def plant_detail(request, plant_id):
    if request.method == 'GET':
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
