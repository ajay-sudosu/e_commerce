from django.urls import path
from account.views import *

app_name = 'account'

urlpatterns = [
    path('register/', account_register, name='register'), ]
