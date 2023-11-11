from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount
from bank.forms.create_bankaccount import BankAccountForm


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
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = BankAccountForm(request.POST)
        user = request.user
        if form.is_valid():
            iban = form.cleaned_data['iban']
            balance = '0'
            currency = form.cleaned_data['currency']
            type = BankAccount.AccauntType.GOLD
            BankAccount.objects.create(iban=iban, owner=user, balance=balance, currency=currency, type=type)
            return redirect('/bank/')
        return render(request, self.template_name, {'form': form})
    
