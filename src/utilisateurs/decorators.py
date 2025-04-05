from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if required_role == 'visualisation':
                if not request.user.is_authenticated:
                    messages.error(request, "Vous devez être connecté pour accéder à ce module.")
                    return redirect('information_home')
            elif required_role == 'gestion':
                if not (request.user.is_authenticated and (request.user.type_membre in ['complexe', 'administrateur'] or request.user.is_superuser)):
                    messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder au module Gestion.")
                    return redirect('information_home')
            elif required_role == 'administration':
                if not (request.user.is_authenticated and (request.user.type_membre == 'administrateur' or request.user.is_superuser)):
                    messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder au module Administration.")
                    return redirect('information_home')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator