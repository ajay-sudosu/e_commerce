from django.urls import path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    path('add/', add, name='add'),
]
