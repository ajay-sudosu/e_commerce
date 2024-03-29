from django.shortcuts import render, get_object_or_404
from store.models import Product, Category


def products_all(request):
    products = Product.is_active_products.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/detail.html', {'product': product})


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'products': products, 'category': category})


def test(request):
    products = Product.is_active_products.all()
    return render(request, 'store/home.html', {'products': products})
