from django import forms 

from bank.models import BankAccount
from shop.models import Purchase, Product


class PurchaseCreateForm(forms.Form):

    quantity = forms.IntegerField(
        label='Количество', 
        widget=forms.NumberInput(attrs={'min': '1'}),
        initial=1
        )

    BankAccount = forms.ModelChoiceField(
        queryset=BankAccount.objects.none(), 
        empty_label=None, 
        widget=forms.Select(attrs={'class': 'form-control'}), 
        label='Счет списания'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PurchaseCreateForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['BankAccount'].queryset = BankAccount.objects.filter(owner=user, type__in=["Gold", "Red"])
            
    
    CHOICES = (
        (0, 'нет'),
        (1, '1 месяц'),
        (2, '2 месяца'),
        (3, '3 месяца'),
    )

    my_field = forms.ChoiceField(
        choices=CHOICES, 
        widget=forms.Select(attrs={'class': 'form-control'}), 
        label='Рассрочка'
    )

    def clean(self):
        cleaned_data = super().clean()
        # quantity = cleaned_data.get('quantity')
        
        return cleaned_data