from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from cart.forms import CartAddProductForm
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    query = request.GET.get('q')
    if query:
        lookups = (Q(name__icontains=query) |
                   Q(description__icontains=query)
                   )
        products = products.filter(lookups)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'pharma_zone/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,

    }
    return render(request, 'pharma_zone/product/detail.html', context)
