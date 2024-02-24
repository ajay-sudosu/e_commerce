from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', all_products, name='all_products'),
    path('item/<slug:slug>/', product_detail, name='product_detail'),
    path('search/<slug:category_slug>/', category_list, name='category_list')
]
