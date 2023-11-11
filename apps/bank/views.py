from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount
from bank.forms.create_bankaccount import BankAccountForm
from bank.methods import IBAN_Generator


class BankMainPage(View):
    """Main page"""

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = request.user
            Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
            Dep_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.DEP).order_by('owner', 'type')
            Red_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.RED).order_by('owner', 'type')
            return render(
                template_name='bank.html',
                request=request,
                context = {
                    'user': user,
                    'Gold_accounts': Gold_accounts,
                    'Dep_accounts' : Dep_accounts,
                    'Red_accounts' : Red_accounts
                }
            )
        else:
            return redirect('login/')

class CreateBankAccountView(View):
    template_name = 'create_bankaccount.html'

    def get(self, request, *args, **kwargs):
        form = BankAccountForm()
        account_type = kwargs.get('account_type', None)
        return render(request, self.template_name, {'form': form, 'account_type': account_type})
    
    def post(self, request, *args, **kwargs):
        form = BankAccountForm(request.POST)
        user = request.user
        account_type = kwargs.get('account_type', None)
        if form.is_valid():
            balance = '0'
            currency = form.cleaned_data['currency']
            if account_type == 'gold':
                type = BankAccount.AccauntType.GOLD
            elif account_type == 'red':
                type = BankAccount.AccauntType.RED
            elif account_type == 'dep':
                type = BankAccount.AccauntType.DEP
            else:
                type = BankAccount.AccauntType.GOLD  # Значение по умолчанию
            BankAccount.objects.create(owner=user, balance=balance, currency=currency, type=type)
            return redirect('/bank/')
        return render(request, self.template_name, {'form': form})
    
