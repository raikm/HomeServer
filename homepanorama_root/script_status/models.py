import django
from django.db import models


class ScriptStatus(models.Model):
    script_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    script_path = models.CharField(max_length=400)
    status_code = models.IntegerField()
    status_text = models.CharField(max_length=300)
    error_text = models.CharField(max_length=300, blank=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)
    # class Meta:
    #     app_label = 'scripts'
    #__str__ method just tells Django what to print when it needs to print out an instance of the model.
    def __str__(self):
        return self.name
