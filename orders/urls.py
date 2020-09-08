from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    path('list/', views.order_list, name='order_list'),
    path('details/<order_id>', views.order_summary, name='order_details')
]
