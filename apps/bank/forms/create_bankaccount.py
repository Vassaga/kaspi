from django import forms 
from bank.models import BankAccount

from typing import Any


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['currency']
        labels = {
            'currency': 'Валюта'
        }
        widgets = {
            'currency': forms.Select(choices=BankAccount.Currencies.choices)
        }

    def clean(self) -> dict[str, Any]:
        return super().clean()