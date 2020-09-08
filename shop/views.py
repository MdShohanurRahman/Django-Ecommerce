from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, Post
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from cart.forms import CartAddProductForm
from django.db.models import Q
from .forms import *


def product_list(request, category_slug=None):
    category = None
    subcategories = None
    childproduct = None
    form = None
    child = None
    categories = Category.objects.all().filter(parent_id=None)
    products = Product.objects.filter(available=True)
    query = request.GET.get('q')
    if query:
        lookups = (Q(name__icontains=query) |
                   Q(description__icontains=query)
                   )
        products = products.filter(lookups)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent_id=category.id)
        products = Product.objects.filter(category=category, available=True)
        childproduct = Product.objects.filter(category=subcategories.first(), available=True)
        form = BookOrderForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "your order is submitted")
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'category': category,
        'subcategories': subcategories,
        'categories': categories,
        'form': form,
        'post': products,
        'child': child,
        'childproduct': childproduct
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    review_form = ProductReviewForm(request.POST or None)
    comment = Comment.objects.filter(post=id)
    if review_form.is_valid():
        instance = review_form.save(commit=False)
        instance.post = product
        instance.name = request.user.username
        instance.save()
        # return reverse ('shop:product_detail', kwargs={'id': id,'slug':slug})
        return redirect(request.META['HTTP_REFERER'])
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'review_form': review_form,
        'comment': comment,
        'star': ['1', '2']
    }
    return render(request, 'shop/product/detail.html', context)


# def book_order(request):
#     form = BookOrderForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect(request.META['HTTP_REFERER'])
#     return render(request)


def show_sub_category(request, category_slug):

    return render(request, "shop/product/subcategory.html",)
