# Exemple d'un décorateur role_required qui permet l'accès si le rôle de l'utilisateur
# est "simple" ou supérieur dans la hiérarchie.
from django.core.exceptions import PermissionDenied

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Supposons que vous avez une hiérarchie des rôles sous forme d'un dictionnaire
            role_hierarchy = {
                'simple': 1,
                'complexe': 2,
                'administrateur': 3,
            }
            user_role = request.user.type_membre  # ou une autre propriété définissant le rôle
            if role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
