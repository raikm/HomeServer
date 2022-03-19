import django
from django.db import models


class Notification(models.Model):
    class Application(models.TextChoices):
        PLANTS = "PL", ("Plants")
        DEVICES = "DE", ("Devices")

    class NotificationStatus(models.TextChoices):
        NEW = "N", ("New")
        READ = "R", ("Read")

    class Status(models.TextChoices):
        BATTERY_LOW = "BL", ("Battery low")
        NO_RESPONSE = "NR", ("No Response")

    id = models.AutoField(primary_key=True)
    application = models.CharField(max_length=100, choices=Application.choices)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(default=django.utils.timezone.now)
    type = models.CharField(max_length=5, choices=Status.choices)
    notificationStatus = models.CharField(
        max_length=100, choices=NotificationStatus.choices
    )
    entity_id = models.CharField(max_length=100)
