from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('register/', account_register, name='register'),
    # user dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path('activate/<slug:uidb64>/<slug:token>/', account_activate, name='activate'), ]
