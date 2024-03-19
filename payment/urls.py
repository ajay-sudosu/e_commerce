from django.urls import path

from payment.views import *

app_name = 'payment'
urlpatterns = [
    path('', basket_view, name='basket'),
    path('webhook', stripe_webhook),
]
