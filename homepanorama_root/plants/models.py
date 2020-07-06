from django.db import models
import django

class Plant(models.Model):
    plant_id = models.IntegerField()
    plantname = models.CharField(max_length=100)
    battery = models.DecimalField(max_digits=4, decimal_places=3)
    version = models.CharField(max_length=40)
    sunlight = models.DecimalField(max_digits=4, decimal_places=3)
    temperature = models.DecimalField(max_digits=4, decimal_places=3)
    moisture = models.DecimalField(max_digits=4, decimal_places=3)
    fertility = models.DecimalField(max_digits=4, decimal_places=3)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    class Meta:
        app_label = 'plants'
    #__str__ method just tells Django what to print when it needs to print out an instance of the model.
    def __str__(self):
        return self.name
