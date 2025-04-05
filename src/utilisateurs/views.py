from django.shortcuts import render, redirect
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

User = get_user_model()


def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
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
