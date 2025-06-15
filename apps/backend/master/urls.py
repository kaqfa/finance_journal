from django.urls import path
from journal.views import login
from journal.views import application as app

app_name = 'journal'

urlpatterns = [
    path('', app.landing_page, name='landing'),
]