from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')