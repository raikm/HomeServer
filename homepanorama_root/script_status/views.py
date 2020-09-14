from django.shortcuts import render
from .models import ScriptStatus
from .serializers import ScriptStatusSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .db_utils import check_existence

@csrf_exempt
@api_view(('PUT', 'GET'))
def script_status_detail(request, script_id):
    if request.method == 'GET':
        if check_existence(script_id):
            script_status = ScriptStatus.objects.get(script_id=script_id)
            serializer = ScriptStatusSerializer(script_status)
            return JsonResponse(serializer.data)
    elif request.method == 'PUT':
        if check_existence(script_id):
            my_obj = ScriptStatus.objects.filter(script_id=script_id)
            my_obj.delete()
        serializer = ScriptStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#TODO: all scripts last statues
