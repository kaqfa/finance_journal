from django.urls import path
from journal.views import login
from journal.views import application as app

app_name = 'journal'

urlpatterns = [
    path('', login.loginView, name='login'),
    path('sign-in', login.signIn, name='signIn'),
    path('register', login.register, name='register'),
    path('forget-password', login.forgetPassword, name='forget_password'),
    path('sign-out', login.signOut, name='sign_out'),
    path('transactions', app.transaction_list, name='transaction_list'),
    path('portos', app.porto_list, name='porto_list'),
    path('porto/<int:porto_id>', app.porto_list, name='porto_detail'),
]