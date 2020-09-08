from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from Mbstu_kenabecha.views import GeneratePdf

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('mainapp.urls')),
    path('AliExpress-Pre-Order', TemplateView.as_view(template_name='main_apps/faq.html'), name='template'),
    path('cart', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('our-shop/', include('shop.urls')),
    path('pharma-zone/', include('pharma_zone.urls')),
    # path('pdf/', GeneratePdf.as_view())

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
