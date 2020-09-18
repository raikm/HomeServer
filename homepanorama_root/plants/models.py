from django.db import models
import django



class Plant(models.Model):
    address = models.CharField(max_length=100)
    battery = models.IntegerField()
    name = models.CharField(max_length=100)
    plant_id = models.IntegerField()
    soil_fertility = models.IntegerField()
    soil_moisture = models.IntegerField()
    sunlight = models.IntegerField()
    temperature = models.DecimalField(max_digits=4, decimal_places=2)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    version = models.CharField(max_length=40)


class SoilFertitlityBorders(models.Model):
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, related_name='soil_fertitlity_borders', on_delete=models.CASCADE)


class SoilMoistureBorders(models.Model):
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, related_name='soil_moisture_borders', on_delete=models.CASCADE)

class SunlightIntensityBorders(models.Model):
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, related_name='sunlight_intensity_borders', on_delete=models.CASCADE)

class TemperatureBorders(models.Model):
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(Plant, related_name='temperature_borders', on_delete=models.CASCADE)
