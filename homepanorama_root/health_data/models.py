from django.db import models
from pyexpat import model


class DayHistory(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    metrics = models.JSONField()
    workouts = models.JSONField()
