from django import forms 
from bank.models import BankAccount, Transfer

from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from typing import Any


class BankAccountWidget(forms.Select):
    def format_option(self, *args, **kwargs):
        option = super().format_option(*args, **kwargs)
        account_pk = option['value']
        try:
            account = BankAccount.objects.get(pk=account_pk)
            option['label'] += f" (Баланс: {account.balance} {account.currency})"
        except BankAccount.DoesNotExist:
            pass  # Обработка исключения, если счет не найден (это может произойти, если вы удалите счет после того, как пользователь выбрал его в форме)
        return option

class TransferSelfForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['outaccount', 'inaccount', 'amount']
        labels = {
            'outaccount': 'Счет списания',
            'inaccount': 'Счет назначения',
            'amount': 'Сумма'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransferSelfForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['outaccount'].queryset = BankAccount.objects.filter(owner=user)
            self.fields['inaccount'].queryset = BankAccount.objects.filter(owner=user)

        # Если выбран счет списания, исключите его из возможных счетов для зачисления
        outaccount = self.fields['outaccount'].widget.value_from_datadict(self.data, self.files, self.add_prefix('outaccount'))
        if outaccount:
            self.fields['inaccount'].queryset = self.fields['inaccount'].queryset.exclude(pk=outaccount)

        # # Используйте кастомный виджет для outaccount
        # self.fields['outaccount'].widget = BankAccountWidget()

    def clean(self):
        cleaned_data = super().clean()
        outaccount = cleaned_data.get('outaccount')
        inaccount = cleaned_data.get('inaccount')

        # Проверьте, что inaccount не равен outaccount
        if outaccount and inaccount and outaccount == inaccount:
            raise forms.ValidationError("Счет списания и счет зачисления не должны совпадать.")

        return cleaned_data