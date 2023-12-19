
""" SHOP ADMIN """


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


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'user', 'price', 'iban', 'purchase_date', 'purchase_type', 'inst_duration', 'monthly_payment', 'next_pay_date', 'remaining_amount', 'pk']
    list_filter = ['product', 'user', 'iban', 'purchase_type', 'inst_duration', 'monthly_payment']
    ordering = ['product', 'quantity', 'user', 'price', 'iban', 'purchase_date', 'purchase_type', 'inst_duration', 'monthly_payment']