from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from basket.context_processors import Basket
from store.models import Product

#
# def basket_summary(request):
#     basket = Basket(request)
#     return render(request, 'basket/summary.html', context={'basket': basket})


def basket_summary(request):
    return render(request, 'basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("productid"))
        productqty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product, productqty)
        basketqty = len(basket)
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get("action") == 'delete':
        product_id = request.POST.get("productid")
        basket.delete(product=product_id)
        basketqty = len(basket)
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get("action") == 'update':
        product_id = int(request.POST.get("productid"))
        productqty = int(request.POST.get("productqty"))
        basket.update(product=product_id, productqty=productqty)
        basketqty = len(basket)
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_total})
        return response
