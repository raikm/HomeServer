import django
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification

BATTERY_BORDER = 20
SOIL_FERTILITY_BORDER = 20
SOIL_MOISTURE_BORDER = 20
TEMP_BORDER = 12


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
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="plant_data",
        on_delete=models.CASCADE,
    )


@receiver(post_save, sender=PlantData)
def notifaction_checkups(sender, instance: PlantData, **kwargs):
    plant = Plant.objects.filter(id=instance.plant_id).first()
    location_data = Locations.objects.get(plant_id=instance.plant_id)
    if plant is None:
        return
    if instance.battery < BATTERY_BORDER and entity_already_exist("BL", "PL", instance.plant_id) == False:
        Notification.objects.create(
            title="Low battery at " + plant.name + " sensor",
            description="Plant sensor @" + location_data.location + " battery running low",
            notificationStatus="N",
            application="PL",
            type="BL",
            entity_id=instance.plant_id
        )
    if instance.soil_fertility < SOIL_FERTILITY_BORDER and entity_already_exist("SFL", "PL", instance.plant_id) == False:
        Notification.objects.create(
            title="Soil fertility from " + plant.name + " is low",
            description="Plant sensor @" + location_data.location +
            " messearing low soil fertility",
            notificationStatus="N",
            application="PL",
            type="SFL",
            entity_id=instance.plant_id
        )
    if instance.soil_moisture < SOIL_MOISTURE_BORDER and entity_already_exist("SML", "PL", instance.plant_id) == False:
        Notification.objects.create(
            title="Soil moisture from " + plant.name + " is low",
            description="Plant sensor @" + location_data.location +
            " messearing low soil moisture",
            notificationStatus="N",
            application="PL",
            type="SML",
            entity_id=instance.plant_id
        )
    if instance.temperature < TEMP_BORDER and entity_already_exist("TL", "PL", instance.plant_id) == False:
        Notification.objects.create(
            title="Temperature from " + plant.name + " is low",
            description="Plant sensor @" + location_data.location +
            " messearing low temperature",
            notificationStatus="N",
            application="PL",
            type="TL",
            entity_id=instance.plant_id
        )


def entity_already_exist(type, application, entity_id):
    return Notification.objects.filter(type=type, application=application, entity_id=entity_id).exists()


class SoilFertitlityBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="soil_fertitlity_borders",
        on_delete=models.CASCADE,
    )


class SoilMoistureBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="soil_moisture_borders",
        on_delete=models.CASCADE,
    )


class SunlightIntensityBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="sunlight_intensity_borders",
        on_delete=models.CASCADE,
    )


class TemperatureBorders(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=100)
    max = models.IntegerField()
    min = models.IntegerField()
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="temperature_borders",
        on_delete=models.CASCADE,
    )


class Locations(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=100)
    location_details = models.CharField(max_length=100)
    location_floor = models.IntegerField()
    plant = models.ForeignKey(
        Plant, null=True, blank=True, related_name="location", on_delete=models.CASCADE
    )


class ValueChanges(models.Model):
    class ValueType(models.TextChoices):
        FERTILITY = "F", ("Fertility")
        MOISTURE = "M", ("Moisture")

    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=2, choices=ValueType.choices)
    date = models.DateTimeField(default=django.utils.timezone.now)
    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="value_changes",
        on_delete=models.CASCADE,
    )


# {
#     "plant_id":1,
#     "battery": 10,
#     "version": "1.0.0",
#     "sunlight": 1000,
#     "temperature": 12,
#     "soil_moisture": 10,
#     "soil_fertility": 540,
#     "timestamp": "2022-03-18T13:22:23"
# }
