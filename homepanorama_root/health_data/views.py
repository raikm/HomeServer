from datetime import date
from sqlite3 import Date

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from health_data.models import DayHistory


@csrf_exempt
@api_view(('POST',))
def save_health_data_export(request):
    export_data = request.data["data"] #'metrics', 'workouts'#
    #extract date
    today = date.today()
    #d1 = today.strftime("%d/%m/%Y")
    # TODO check if date in db already exist
        # if yes delete entry 
    # save entry into db
    DayHistory.objects.create(date=today, metrics=export_data['metrics'], workouts=export_data['workouts'])
    return Response("healthdata export got saved", status=status.HTTP_200_OK)
