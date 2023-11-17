from django import forms 
from bank.models import BankAccount, Transfer

from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from typing import Any


class TransferAnyForm(forms.ModelForm):

    account_number = forms.CharField(label='Номер счета')

    class Meta:
        model = Transfer
        fields = ['outaccount', 'outamount']
        labels = {
            'outaccount': 'Счет списания',
            'outamount': 'Сумма'
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferAnyForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['outaccount'].queryset = BankAccount.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get('account_number')

        if account_number:
            try:
                inaccount = BankAccount.objects.get(iban=account_number)
                cleaned_data['inaccount'] = inaccount
            except BankAccount.DoesNotExist:
                raise forms.ValidationError("Счет с таким номером не найден.")
        
        return cleaned_data