from django.contrib import admin

# Register your models here.

from bank.models import (
    BankAccount,
    Transfer
)

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['iban', 'owner', 'balance', 'currency',  'type', 'is_active']
    list_filter = ['currency',  'type', 'is_active', 'owner']
    ordering = ['iban', 'owner', 'currency', 'type', 'is_active']

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['pk', 'datetime', 'user', 'amount', 'outaccount',  'inaccount']
    list_filter = ['datetime',  'user', 'amount']
    ordering = ['datetime', 'user', 'amount', 'outaccount',  'inaccount']