from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings

@login_required
def transaction_list(request):
    return render(request, 'pages/transaction_list.html')

@login_required
def porto_list(request):
    return render(request, 'pages/portfolio_list.html')

@login_required
def porto_detail(request, porto_id):
    return render(request, 'pages/portfolio_detail.html', {'porto_id': porto_id})