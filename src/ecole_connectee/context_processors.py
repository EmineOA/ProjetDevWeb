from src.administration.models import Apparence

def appearance_context(request):
    appearance = None
    try:
        appearance = Apparence.objects.get(id=1)
    except Apparence.DoesNotExist:
        pass
    return {'appearance': appearance}
