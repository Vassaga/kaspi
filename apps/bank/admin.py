from django.contrib import admin

# Register your models here.

from bank.models import (
    BankAccount,
)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['iban', 'owner', 'balance', 'currency',  'type', 'is_active']
    list_filter = ['currency',  'type', 'is_active']
    ordering = ['iban', 'owner', 'currency', 'type', 'is_active']