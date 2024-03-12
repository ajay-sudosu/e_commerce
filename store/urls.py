from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', products_all, name='product_all'),
    path('<slug:slug>', product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', category_list, name='category_list'),
    path('basket', category_list, name='summary'),
    path('test/', test, name='test'),
]
