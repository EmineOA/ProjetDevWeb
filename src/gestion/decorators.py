from django.contrib.auth.decorators import user_passes_test

def gestion_access_required(user):
    return user.is_authenticated and user.type_membre in ['complexe', 'administrateur']

# Pour l'utiliser directement sur vos vues, vous pouvez également créer un décorateur combiné :
gestion_required = user_passes_test(gestion_access_required, login_url='login')
