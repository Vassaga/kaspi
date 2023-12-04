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
            try:
                inaccount = BankAccount.objects.filter(Q(owner__number=account_number) & Q(type='Gold'))
                cleaned_data['inaccount'] = inaccount
            except BankAccount.DoesNotExist:
                raise forms.ValidationError("Клиент таким номером не найден.")
        
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
            try:
                inaccount = BankAccount.objects.filter(Q(iban=account_number) & Q(type='Gold'))
                cleaned_data['inaccount'] = inaccount
                if len(inaccount) <1:
                    raise forms.ValidationError("Счет с таким номером не найден.")
            except:
                # Обработка исключений
                pass


        return cleaned_data