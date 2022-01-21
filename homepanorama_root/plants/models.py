import django
from django.db import models


class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=40)
    address = models.CharField(max_length=100)




class PlantData(models.Model):
    id = models.AutoField(primary_key=True)
    battery = models.IntegerField()
    soil_fertility = models.IntegerField()
    soil_moisture = models.IntegerField()
    sunlight = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='plant_data', on_delete=models.CASCADE)


class SoilFertitlityBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='soil_fertitlity_borders', on_delete=models.CASCADE)


class SoilMoistureBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='soil_moisture_borders', on_delete=models.CASCADE)


class SunlightIntensityBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='sunlight_intensity_borders', on_delete=models.CASCADE)


class TemperatureBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='temperature_borders', on_delete=models.CASCADE)


class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    location_details = models.CharField(max_length=100)
    location_floor = models.IntegerField()
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='location', on_delete=models.CASCADE)


class ValueChanges(models.Model):
    class ValueType(models.TextChoices): 
        FERTILITY = 'F', ('Fertility')
        MOISTURE = 'M', ('Moisture')
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=2,choices=ValueType.choices)
    date = models.DateTimeField(default=django.utils.timezone.now)
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='value_changes', on_delete=models.CASCADE)
