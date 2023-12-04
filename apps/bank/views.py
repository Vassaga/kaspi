
''' BANK VIEWS '''

from django.shortcuts import render, redirect
from django.views import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
# Create your views here.

from auths.models import MyUser
from bank.models import BankAccount, Transfer
from bank.forms.create_bankaccount import BankAccountForm
from bank.forms.TransferSelfBankAccForm import TransferSelfForm
from bank.forms.TransferAnyBankAccForm import TransferAnyFormByIBAN, TransferAnyFormByNumber
from bank.currency_converter import currency_converter
from shop.models import Purchase


class BankMainPageView(View):

    """ ГЛАВНАЯ СТРАНИЦА БАНКА ПОЛЬЗОВАТЕЛЯ. """

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = request.user   # получаем авторизованного пользователя
            # вытаскиваем типы счетов:
            Gold_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.GOLD).order_by('owner', 'type')
            Dep_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.DEP).order_by('owner', 'type')
            Red_accounts = BankAccount.objects.filter(owner=user, type=BankAccount.AccauntType.RED).order_by('owner', 'type')
            Inst = Purchase.objects.filter(user=user, remaining_amount__gt=0)
            BadInst = Purchase.objects.filter(
                user=user,
                next_pay_date__lte=timezone.now()
            )
            print(Inst)
            print(BadInst)
            return render(
                template_name='bank.html',
                request=request,
                context = {
                    'user': user,
                    'inst': Inst,
                    'badinst': BadInst,
                    'Gold_accounts': Gold_accounts,
                    'Dep_accounts' : Dep_accounts,
                    'Red_accounts' : Red_accounts
                }
            )
        else:
            return redirect('login/')

class CreateBankAccountView(View):

    """
    СТРАННИЦА СОЗДАНИЯ СЧЕТА.

        Параметры:
        - account_type 
        Извлекаем информацию о типе счета из параметров запроса
        (данные о типе создаваемого счета сидят в ссылках на странице выбора создаваемого счета)

        -  user = request.user:
        Получаем авторизованного пользователя, что бы отображать (обрабатывать) именно его счета

    """
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
                type = BankAccount.AccauntType.GOLD  # Значение по умолчанию - нужно ли нам это?
            BankAccount.objects.create(owner=user, balance=balance, currency=currency, type=type)
            return redirect('/bank/')
        return render(request, self.template_name, {'form': form})
    
    
class TransfersPageView(View):

    """ СТРАННИЦА ПЕРЕВОДОВ. """

    template_name = 'TransfersPage.html'

    def get(self, request):
        return render(request, self.template_name)
    

class TransferSelfBankAccountsView(View):

    """ СТРАННИЦА ПЕРЕВОДОВ МЕЖДУ СВОИМИ СЧЕТАМИ. """

    template_name = 'TransferSelfBankAccounts.html'

    def get(self, request):
        form = TransferSelfForm(user=request.user)
        return render(request, self.template_name, {'form': form,})
    
    def post(self, request, *args, **kwargs):
        form = TransferSelfForm(request.POST)
        user = request.user
        if form.is_valid():
            outamount = form.cleaned_data['outamount']
            outaccount = form.cleaned_data['outaccount']
            outaccount_object = form.fields['outaccount'].queryset.get(pk=outaccount.pk)
            inaccount = form.cleaned_data['inaccount']
            inaccount_object = form.fields['inaccount'].queryset.get(pk=inaccount.pk)
            inamount = currency_converter(float(outamount), str(outaccount_object.currency), str(inaccount_object.currency))
            try:
                if outaccount_object.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('success/')
                else:
                    inaccount_object.balance += inamount
                    outaccount_object.balance -= outamount
                    outaccount_object.save()  # Сохраняем изменения в базе данных
                    inaccount_object.save()   # Сохраняем изменения в базе данных
                    incurrency = inaccount_object.currency
                    outcurrency = outaccount_object.currency
                    Transfer.objects.create(
                        outaccount=outaccount_object, 
                        inaccount=inaccount_object,
                        outamount=outamount,
                        inamount=inamount,
                        outcurrency=outcurrency,
                        incurrency=incurrency,
                        outbalance=outaccount_object.balance,
                        inbalance=inaccount_object.balance)
            except:
                # Обработка исключений
                pass
            messages.success(request, 'Транзакция успешно выполнена.')        
            return redirect('success/')
        return render(request, self.template_name, {'form': form})

class TransferSuccessView(View):

    """ СТРАННИЦА О СТАТУСЕ ПЕРЕВОДОВ МЕЖДУ СВОИМИ СЧЕТАМИ. """

    template_name = 'Transfer_done.html'

    def get(self, request):
        return render(request, self.template_name)
    
    
class TransfersHistoryView(View):

    """ СТРАННИЦА ИСТОРИИ ПЕРЕВОДОВ. """

    def get(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = request.user   
            Transfers = Transfer.objects.filter(Q(transaction_type='Transfer') & Q(outaccount__owner=user)).order_by('-datetime')
            return render(
                template_name = 'Transfer_history.html',
                request=request,
                context = {
                    'user': user,
                    'Transfers': Transfers,
                }
            )
        else:
            return redirect('login/')
        

class TransferAnyChoicePageView(View):

    """ СТРАННИЦА ВЫБОРА ПЕРЕВОДА ДЛЯ КЛИЕНТА КАСПИ. """

    template_name = 'TransferAnyChoice.html'

    def get(self, request):
        return render(request, self.template_name)

class TransferAnyBankAccountsViewByNumber(View):

    """ СТРАННИЦА ПЕРЕВОДОВ НА СЧЕТ ДРУГОГО КЛИЕНТА КАСПИ. """

    template_name = 'TransferAnyBankAccounts1.html'

    def get(self, request):
        form = TransferAnyFormByNumber(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = TransferAnyFormByNumber(request.POST)
        user = request.user
        if form.is_valid():
            outamount = form.cleaned_data['outamount']
            outaccount = form.cleaned_data['outaccount']
            inaccount = form.cleaned_data['inaccount'][0]
            print(inaccount)
            inamount = currency_converter(float(outamount), str(outaccount.currency), str(inaccount.currency))
            try:
                if outaccount.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('/transfers/any/success/')
                else:
                    inaccount.balance += inamount
                    outaccount.balance -= outamount
                    outaccount.save()
                    inaccount.save()
                    incurrency = inaccount.currency
                    outcurrency = outaccount.currency
                    Transfer.objects.create(
                         outaccount=outaccount, 
                         inaccount=inaccount,
                         outamount=outamount, 
                         inamount=inamount,
                         outcurrency=outcurrency,
                         incurrency=incurrency,
                         outbalance=outaccount.balance,
                         inbalance=inaccount.balance)
            except:
                # Обработка исключений
                pass
            messages.success(request, 'Транзакция успешно выполнена.')        
            return redirect('/transfers/any/success/')
        return render(request, self.template_name, {'form': form})
    
class TransferAnyBankAccountsViewByIBAN(View):

    """ СТРАННИЦА ПЕРЕВОДОВ НА СЧЕТ ДРУГОГО КЛИЕНТА КАСПИ. """

    template_name = 'TransferAnyBankAccounts.html'

    def get(self, request):
        form = TransferAnyFormByIBAN(user=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = TransferAnyFormByIBAN(request.POST)
        user = request.user
        if form.is_valid():
            outamount = form.cleaned_data['outamount']
            outaccount = form.cleaned_data['outaccount']
            inaccount = form.cleaned_data['inaccount'][0]
            print(len(inaccount))
            inamount = currency_converter(float(outamount), str(outaccount.currency), str(inaccount.currency))
            try:
                if outaccount.balance < outamount:
                    messages.error(request, 'Недостаточно средств на счете списания.')
                    return redirect('/transfers/any/success/')
                else:
                    inaccount.balance += inamount
                    outaccount.balance -= outamount
                    outaccount.save()
                    inaccount.save()
                    incurrency = inaccount.currency
                    outcurrency = outaccount.currency
                    Transfer.objects.create(
                         outaccount=outaccount, 
                         inaccount=inaccount,
                         outamount=outamount, 
                         inamount=inamount,
                         outcurrency=outcurrency,
                         incurrency=incurrency,
                         outbalance=outaccount.balance,
                         inbalance=inaccount.balance)
            except:
                # Обработка исключений
                pass
            messages.success(request, 'Транзакция успешно выполнена.')        
            return redirect('/transfers/any/success/')
        return render(request, self.template_name, {'form': form})
    

class UserInstsView(View):

    """ СТРАННИЦА РАССРОЧЕК ПОЛЬЗОВАТЕЛЯ. """
    template_name = 'UserInsts.html'

    def get(self, request):
        user = request.user
        Inst = Purchase.objects.filter(user=user, remaining_amount__gt=0)
        BadInst = Purchase.objects.filter(
            user=user,
            next_pay_date__lte=timezone.now()
        )
        return render(
            request, 
            self.template_name, 
            context = {
                'user': user,
                'inst': Inst,
                'badinst': BadInst,
            })