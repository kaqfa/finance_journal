from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings

def landing_page(request):
    return render(request, 'pages/landing.html')