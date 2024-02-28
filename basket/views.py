from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from basket.context_processors import Basket
from store.models import Product


def basket_summary(request):
    data = request.session.get("skey")
    return render(request, 'basket/summary.html')


def basket_add(request):
    basket = Basket(request)
    if request.POST.get("action") == 'post':
        product_id = int(request.POST.get("productid"))
        productqty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product, productqty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response
