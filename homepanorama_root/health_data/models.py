import dataclasses
from typing import List, Optional

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from pyexpat import model


class DayHistory(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()


class DailyMetrics(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    units = models.CharField(max_length=1000)
    # data =
    day_history = models.ForeignKey(DayHistory,
                                    related_name='daily_metrics', on_delete=models.CASCADE)
