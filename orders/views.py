from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from django.core.mail import send_mail


def order_create(request):
    global order
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            email = order.email
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            subject = 'MBSTU Bazar | Customer Invoice'
            msg = '''Thanks for shopping with us.We will call you as soon as possible.If any query please let us know.'''
            from_email = settings.EMAIL_HOST_USER
            send_mail(subject,
                      msg + '\nYour invoice number is ' + str(order.id) + '\nTotal due BDT ' + str(
                          order.get_total_cost()),
                      from_email,
                      [email],
                      fail_silently=False,
                      )
            order_item = OrderItem.objects.filter(order=order.id)  # order item
        return render(request, 'orders/order/created.html', {'order': order, 'order_item': order_item})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})


@login_required
def order_list(request):
    if request.user.is_superuser:
        order_obj = Order.objects.all()
        context = {
            'order_obj': order_obj
        }
        return render(request, 'orders/orders-list.html', context)
    else:
        raise Http404('You are not authorized to access this page')


@login_required
def order_summary(request, order_id):
    if request.user.is_superuser:
        order_id = get_object_or_404(Order, id=order_id)
        obj = OrderItem.objects.filter(order=order_id)
        context = {
            'order': obj,
            'order_id': order_id,
        }
        return render(request, 'orders/order-details.html', context)
    else:
        raise Http404('You are not authorized to access this page')
