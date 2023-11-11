from django import forms 
from bank.models import BankAccount

from django.core.exceptions import ValidationError
from typing import Any


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['iban', 'currency', 'is_active']
        labels = {
            'iban': 'Номер счета',
            'currency': 'Валюта',
            'is_active': 'Активен',
        }
        widgets = {
            'currency': forms.Select(choices=BankAccount.Currencies.choices)
        }

    def clean(self) -> dict[str, Any]:
        return super().clean()
    
    def clean_number(self):   # нужно доработать разные варианты ошибок номера, пустое поле, некорректный номер и т.д.
        data: str = self.cleaned_data['number']
        if MyUser.objects.filter(number=data).exists() == True:
            raise ValidationError('пользователь с таким номером уже зарегистрирован')
        return data