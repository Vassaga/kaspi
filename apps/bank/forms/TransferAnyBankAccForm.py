from django import forms 
from bank.models import BankAccount, Transfer

from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from typing import Any
from django.db.models import Q


class TransferAnyFormByNumber(forms.ModelForm):

    account_number = forms.CharField(label='Телефон клиента каспи')
    
    class Meta:
        model = Transfer
        fields = ['outaccount', 'outamount']
        labels = {
            'outaccount': 'Счет списания',
            'outamount': 'Сумма'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferAnyFormByNumber, self).__init__(*args, **kwargs)

        if user:
            self.fields['outaccount'].queryset = BankAccount.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get('account_number')

        if account_number:
            inaccount = BankAccount.objects.filter(Q(owner__number=account_number) & Q(type='Gold'))
            if not inaccount.exists():
                raise ValidationError("Клиент с таким номером не найден или не имеет счета Каспи Gold.")
            cleaned_data['inaccount'] = inaccount.first()
        return cleaned_data
    
    
class TransferAnyFormByIBAN(forms.ModelForm):

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
        super(TransferAnyFormByIBAN, self).__init__(*args, **kwargs)

        if user:
            self.fields['outaccount'].queryset = BankAccount.objects.filter(owner=user)

    def clean(self):
        cleaned_data = super().clean()
        account_number = cleaned_data.get('account_number')

        if account_number:
            inaccount = BankAccount.objects.filter(Q(iban=account_number) & Q(type='Gold'))
            if not inaccount.exists():
                raise ValidationError("Клиент с таким счетом Каспи Gold не найден.")
            cleaned_data['inaccount'] = inaccount.first()



        return cleaned_data