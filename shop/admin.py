from django.contrib import admin
from .models import Category, Product, Comment,BookOrder


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'past_price', 'stock', 'available', 'created_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'past_price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)
admin.site.register(BookOrder)
