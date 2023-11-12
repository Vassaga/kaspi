from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount, Transfer
from bank.forms.create_bankaccount import BankAccountForm
from bank.forms.TransferSelfBankAccForm import TransferSelfForm
from bank.methods import IBAN_Generator


class BankMainPageView(View):
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

    """Create Bank Account page"""

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
    
class TransfersPageView(View):

    """Transfers page"""

    template_name = 'TransfersPage.html'

    def get(self, request):
        return render(request, self.template_name)
    

class TransferSelfBankAccountsView(View):

    """Transfers page"""

    template_name = 'TransferSelfBankAccounts.html'

    def get(self, request):
        form = TransferSelfForm(user=request.user)
        return render(request, self.template_name, {'form': form,})
    
    def post(self, request, *args, **kwargs):
        form = TransferSelfForm(request.POST)
        user = request.user
        if form.is_valid():
            amount = form.cleaned_data['amount']
            outaccount = form.cleaned_data['outaccount']
            outaccount_object = form.fields['outaccount'].queryset.get(pk=outaccount.pk)
            inaccount = form.cleaned_data['inaccount']
            inaccount_object = form.fields['inaccount'].queryset.get(pk=inaccount.pk)
            
            try:
                if outaccount_object.balance < amount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('success/')
                else:
                    # Обновляем баланс объекта outaccount
                    outaccount_object.balance -= amount
                    inaccount_object.balance += amount
                    outaccount_object.save()  # Сохраняем изменения в базе данных
                    inaccount_object.save()
                    Transfer.objects.create(user=user, amount=amount, outaccount=outaccount_object, inaccount=inaccount_object)
            except:
                # Обработка исключений
                pass
            messages.success(request, 'Транзакция успешно выполнена.')        
            return redirect('success/')
        return render(request, self.template_name, {'form': form})

class TransferSuccessView(View):
    template_name = 'Transfer_done.html'

    def get(self, request):
        return render(request, self.template_name)