from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Utilisateur
from .forms import ProfileUpdateForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect

User = get_user_model()

def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.type_membre = "simple",
                user.is_active = False  # Désactive le compte jusqu'à activation par e-mail
                user.save()

                # Envoi de l'e-mail de confirmation
                current_site = get_current_site(request)
                mail_subject = 'Confirmez votre inscription'
                message = render_to_string('inscription/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()

                messages.success(request,
                                 "Inscription réussie ! Veuillez vérifier votre boîte mail pour activer votre compte.")
                return redirect('inscription')
            except IntegrityError:
                messages.error(request,
                               "Un utilisateur avec ce nom existe déjà. Veuillez choisir un autre nom d'utilisateur.")
        else:
            # Affiche les erreurs du formulaire dans des messages (toast)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form[field].label}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription/inscription.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Votre compte a été activé avec succès. Vous pouvez maintenant vous connecter.')
    else:
        return HttpResponse('Le lien d’activation est invalide !')

@login_required
def profile_view(request, user_id=None):
    """
    Affiche le profil d'un utilisateur.
    - Si un user_id est fourni et que l'utilisateur connecté est administrateur, on affiche le profil correspondant.
    - Sinon, on affiche le profil de l'utilisateur connecté.
    """
    if user_id and request.user.is_superuser:
        user_profile = get_object_or_404(Utilisateur, id=user_id)
    else:
        user_profile = request.user

    # On affiche la partie privée uniquement si l'utilisateur consulte son propre profil ou s'il est admin
    show_private = request.user == user_profile or request.user.is_superuser

    context = {
        'user_profile': user_profile,
        'show_private': show_private,
    }
    return render(request, 'utilisateurs/profile.html', context)

@login_required
def profile_edit(request):
    user_profile = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileUpdateForm(instance=user_profile)
    return render(request, 'utilisateurs/profile_edit.html', {'form': form})

@login_required
def logout_confirm(request):
    if request.method == "POST":
        if "confirm" in request.POST:
            # Déconnecter l'utilisateur et rediriger vers le module information
            logout(request)
            return redirect("information_home")
        else:
            # Annuler : rediriger vers la page précédente ou une page par défaut
            previous_url = request.META.get("HTTP_REFERER", "information_home")
            return redirect(previous_url)
    return render(request, "logout_confirm.html")
