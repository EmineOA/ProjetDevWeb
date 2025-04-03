from django.shortcuts import render

def inscription(request):
    return render(request, 'utilisateurs/inscription.html')
