from .models import ScriptStatus

def check_existence(script_id):
    try:
        ScriptStatus.objects.get(script_id=script_id)
        return True
    except ScriptStatus.DoesNotExist:
        return False
