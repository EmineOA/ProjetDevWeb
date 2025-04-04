from src.administration.models import Apparence

def appearance(request):
    try:
        # On suppose qu'il y a une seule instance, identifiée par id=1
        app = Apparence.objects.get(id=1)
    except Apparence.DoesNotExist:
        app = None
    return {'appearance': app}
