
''' BANK ADMIN '''

from django.contrib import admin

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
    list_display = ['pk', 'datetime', 'amount', 'currency', 'outaccount_iban',  'inaccount_iban', 'balance']
    list_filter = ['datetime', 'amount', 'currency']
    ordering = ['datetime', 'amount', 'currency']

    def outaccount_iban(self, obj):
        return obj.outaccount.iban
    
    def inaccount_iban(self, obj):
        return obj.inaccount.iban
    
    outaccount_iban.short_description = 'Исходящий счет'
    inaccount_iban.short_description = 'Входящий счет'