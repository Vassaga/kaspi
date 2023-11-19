from django.contrib import admin

from shop.models import (
    Category,
    Product,
    Purchase
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']
    list_filter = ['name']
    ordering = ['name', 'pk']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'rating', 'pk']
    list_filter = ['name', 'category', 'price', 'quantity', 'rating']
    ordering = ['name', 'category', 'price', 'quantity', 'rating', 'pk']