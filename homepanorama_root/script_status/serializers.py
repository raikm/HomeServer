from rest_framework import serializers

from .models import ScriptStatus

class ScriptStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScriptStatus
        fields = ('script_id', 'name', 'script_path', 'status_code', 'status_text', 'error_text', 'timestamp')
